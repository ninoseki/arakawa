import { DataType } from 'apache-arrow'

type RowTransform = (row: any) => any

const pick = (fieldNames: string[], row: any): any => {
  const result: any = {}
  for (const name of fieldNames) {
    if (Object.hasOwn(row, name)) {
      result[name] = row[name]
    }
  }
  return result
}

/*
This class handled converting some of the more complex Arrow types into something we
can display within the browser, e.g. dates and big-ints.

It is constructed with the table field types, and these are used to dynamically build a list of
row transforms - coerceRow takes a row from the table, picks out only the known field names, and
then runs it through each transform in turn to produce a JS compatible representation of it.

Within the class constructor we iterate over the field names, looking for complex types we need to
process. In these cases, we generate a new transform function that processes and modifies that
individual field in the row, and add it to the list of transforms.

Eventually we end up with a dynamically-built list of transforms where each one will match its own
field and process it, passing the modified row along to the next, in the order the fields were
declared on the schema.
*/
export class Coerce {
  private fieldNames: string[] = []
  private transforms: RowTransform[] = []

  public coerceRow = (row: any) => {
    let result = pick(this.fieldNames, row)
    for (const transform of this.transforms) {
      result = transform(result)
    }
    return result
  }

  public constructor(schemaFields: any[]) {
    for (const field of schemaFields) {
      if (DataType.isTimestamp(field)) {
        this.composeTimestampField(field)
      } else if (DataType.isInt(field)) {
        this.composeIntField(field)
      } else if (DataType.isFloat(field)) {
        this.composeFloatField(field)
      }

      this.fieldNames.push(field.name)
    }
  }

  private composeIntField(_field: any) {
    // Currently a no-op: 64-bit ints pass through unchanged.
  }

  private composeFloatField(field: any) {
    this.transforms.push((row: any) => {
      const val = row[field.name]
      if (val) {
        row[field.name] = parseFloat(val)
      }
      return row
    })
  }

  private composeTimestampField(field: any) {
    if (
      // only handle UTC or local timetamps
      field.type.timezone === null ||
      field.type.timezone === 'UTC'
    ) {
      // It seems that our version of the arrow library
      // coerceRows all timestamp to millisecond resolution with
      // a normal JS Number representation regardless of the
      // resolution set on the field type metadata.
      // This is unlike the examples seen on the web for handling
      // timestamps which presumably work with an earlier version.
      // Therefore we do not need to check the 'field.type.unit' property
      // against 'TimeUnit', we can simply always pass the value to
      // 'new Date()'...
      this.transforms.push((row: any) => {
        const val = row[field.name]
        if (val) {
          row[field.name] = new Date(val).toISOString()
        }
        return row
      })
    }
  }
}
