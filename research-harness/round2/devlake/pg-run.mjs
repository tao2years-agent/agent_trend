import { pathToFileURL } from 'node:url'
import { readFile } from 'node:fs/promises'

const [libraryPath, workloadPath] = process.argv.slice(2)
const { PGlite } = await import(pathToFileURL(libraryPath).href)
const db = new PGlite()
try {
  const workload = JSON.parse(await readFile(workloadPath, 'utf8'))
  const version = (await db.query('SELECT version() AS version')).rows[0].version
  const result = {}
  for (const row of workload) {
    await db.exec(row.fixture)
    const value = (await db.query(row.query)).rows[0].change_failure_rate
    result[row.id] = value === null ? null : Number(value)
  }
  console.log(JSON.stringify({ version, result }))
} finally {
  await db.close()
}
