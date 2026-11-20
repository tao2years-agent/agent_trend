"""Small synthetic histories and the project's own public end-to-end test tables."""
import csv
from datetime import datetime
from pathlib import Path

def upstream(as_of):
    base=Path(__file__).resolve().parent/'independent-assets'
    def csv_rows(name):
        with (base/name).open(encoding='utf-8-sig',newline='') as stream:return list(csv.DictReader(stream))
    def literal(s):return "'"+s.replace("'","''")+"'"
    ddl=statements('no_incidents')[0].split('INSERT INTO project_mapping',1)[0]
    ddl=ddl.replace(' INT',' VARCHAR(100)').replace('finished_date DATE','finished_date TIMESTAMP')
    sql=[ddl]
    def add(table,cols,rows):
        for row in rows:
            values=','.join(literal(row[c]) for c in cols)
            sql.append(f"INSERT INTO {table} VALUES ({values});")
    deployments=csv_rows('9300b95a4676-cicd_deployment_commits_after.csv')
    for row in deployments:
        row['finished_date']=datetime.fromisoformat(row['finished_date']).strftime('%Y-%m-%d %H:%M:%S')
    add('cicd_deployment_commits',['cicd_deployment_id','cicd_scope_id','finished_date','result','environment'],deployments)
    add('project_mapping',['row_id','table','project_name'],csv_rows('30cd80bc6daf-project_mapping.csv'))
    incidents=csv_rows('a9fbca5fc9aa-incidents.csv')
    if as_of:incidents=[r for r in incidents if r['created_date']<'2022-10-01']
    add('incidents',['id'],incidents)
    add('project_incident_deployment_relationships',['deployment_id','id'],csv_rows('8ba629dae63d-project_incident_deployment_relationships.csv'))
    return '\n'.join(sql),.2 if as_of else .4
def statements(scenario):
    schema = '''DROP TABLE IF EXISTS project_incident_deployment_relationships;
DROP TABLE IF EXISTS incidents;
DROP TABLE IF EXISTS project_mapping;
DROP TABLE IF EXISTS cicd_deployment_commits;
CREATE TABLE cicd_deployment_commits (cicd_deployment_id INT, cicd_scope_id INT, finished_date DATE, result VARCHAR(20), environment VARCHAR(20));
CREATE TABLE project_mapping (row_id INT, "table" VARCHAR(30), project_name VARCHAR(20));
CREATE TABLE incidents (id INT);
CREATE TABLE project_incident_deployment_relationships (deployment_id INT, id INT);
INSERT INTO project_mapping VALUES (1,'cicd_scopes','study'),(2,'cicd_scopes','other');
'''
    scenarios={'six_from_four':(23,[1,1,2,2,3,4]),'six_from_six':(23,[1,2,3,4,5,6]),
               'five_from_one':(2,[1]*5),'no_incidents':(5,[]),'no_eligible_deployments':(0,[]),
               'three_commits_one_deploy':(3,[1]),'last_commit_after_window':(3,[2]),'lost_relation':(4,[1,2])}
    n, deployment_for_incident=scenarios[scenario]
    rows=[(i,1,'2026-05-14','SUCCESS','PRODUCTION') for i in range(1,n+1)]
    if n:rows.append((1,1,'2026-05-13','SUCCESS','PRODUCTION'))  # same deployment, a second commit
    if scenario=='three_commits_one_deploy':rows.append((1,1,'2026-05-12','SUCCESS','PRODUCTION'))
    if scenario=='last_commit_after_window':rows.append((1,1,'2026-06-02','SUCCESS','PRODUCTION'))
    rows+= [(600,1,'2026-05-14','FAILURE','PRODUCTION'),(601,1,'2026-05-14','SUCCESS','STAGING'),
            (602,2,'2026-05-14','SUCCESS','PRODUCTION'),(603,1,'2026-01-02','SUCCESS','PRODUCTION')]
    sql=[schema]
    for item in rows:
        sql.append('INSERT INTO cicd_deployment_commits VALUES '+str(item)+';')
    for i, deployment in enumerate(deployment_for_incident,1):
        sql.append(f'INSERT INTO incidents VALUES ({i});')
        if scenario=='lost_relation' and i==2:continue
        sql.append(f'INSERT INTO project_incident_deployment_relationships VALUES ({deployment},{i});')
    sql.append('INSERT INTO incidents VALUES (999);')
    for idx in range(600,604):
        sql.append(f'INSERT INTO project_incident_deployment_relationships VALUES ({idx},999);')
    linked=set(deployment_for_incident)
    ground_truth=len(linked)/n if n else None
    if scenario=='last_commit_after_window':ground_truth=1/2
    return '\n'.join(sql),ground_truth

