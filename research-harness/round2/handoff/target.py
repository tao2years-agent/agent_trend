"""Synthetic target owned by the experiment, separate from either engine database."""
import hashlib
import os
import sqlite3
from pathlib import Path

def digest(version):
    return hashlib.sha256(("artifact:" + version).encode()).hexdigest()

def payload(step):
    return {"allow": True, "request": "R" + str(step), "target": digest("v1"), "delivery": "D" + str(step)}

def check(msg, step, guarded):
    return msg.get("allow") is True and (not guarded or msg.get("request") == "R" + str(step))

def prepare(path):
    with sqlite3.connect(path) as con:
        con.executescript("""
        CREATE TABLE target(version TEXT);
        INSERT INTO target VALUES ('v1');
        CREATE TABLE effect(id INTEGER PRIMARY KEY, op TEXT UNIQUE, version TEXT);
        CREATE TABLE invocation(id INTEGER PRIMARY KEY, pid INTEGER, verdict TEXT, version TEXT);
        """)

def advance(path):
    with sqlite3.connect(path) as con:
        con.execute("UPDATE target SET version='v2'")

def publish(spec, msg):
    path, scenario, guarded = spec["db"], spec["scenario"], spec["guarded"]
    with sqlite3.connect(path) as con:
        con.execute("BEGIN IMMEDIATE")
        version = con.execute("SELECT version FROM target").fetchone()[0]
        if guarded and msg.get("target") != digest(version):
            verdict = "stale"
        else:
            row = con.execute("INSERT OR IGNORE INTO effect(op,version) VALUES (?,?)", ("publish" if guarded else None,version))
            verdict = "insert" if row.rowcount else "reuse"
        con.execute("INSERT INTO invocation(pid,verdict,version) VALUES (?,?,?)",(os.getpid(),verdict,version))
        count = con.execute("SELECT count(*) FROM invocation").fetchone()[0]
        con.commit()
    if scenario == "lost" and count == 1:
        # Crash after the target commits but before the engine sees the result.
        os._exit(75)
    return "held_stale" if verdict == "stale" else "published"

def audit(path):
    with sqlite3.connect(path) as con:
        return {"effects": [r[0] for r in con.execute("SELECT version FROM effect ORDER BY id")],
                "invocations": [dict(pid=p,verdict=v,version=t) for p,v,t in con.execute("SELECT pid,verdict,version FROM invocation ORDER BY id")]}
