import { Field, Float64, Int32, Int64, TimestampMillisecond, Utf8 } from 'apache-arrow'
import { describe, expect, it } from 'vitest'

import { Coerce } from '../../../src/data-model/datatable/Coerce'

describe('Coerce', () => {
  it('only keeps known field names on the row', () => {
    const coerce = new Coerce([new Field('name', new Utf8())])
    const result = coerce.coerceRow({ name: 'foo', extra: 'bar' })
    expect(result).toEqual({ name: 'foo' })
  })

  it('leaves plain (e.g. string/utf8) fields untouched', () => {
    const coerce = new Coerce([new Field('name', new Utf8())])
    const result = coerce.coerceRow({ name: 'foo' })
    expect(result).toEqual({ name: 'foo' })
  })

  it('parses float fields to numbers', () => {
    const coerce = new Coerce([new Field('score', new Float64())])
    const result = coerce.coerceRow({ score: '1.5' })
    expect(result).toEqual({ score: 1.5 })
  })

  it('leaves falsy float values untouched', () => {
    const coerce = new Coerce([new Field('score', new Float64())])
    expect(coerce.coerceRow({ score: 0 })).toEqual({ score: 0 })
    expect(coerce.coerceRow({ score: null })).toEqual({ score: null })
    expect(coerce.coerceRow({ score: undefined })).toEqual({ score: undefined })
  })

  it('passes through 32-bit int fields unchanged', () => {
    const coerce = new Coerce([new Field('count', new Int32())])
    const result = coerce.coerceRow({ count: 42 })
    expect(result).toEqual({ count: 42 })
  })

  it('passes through 64-bit int fields unchanged (no-op)', () => {
    const coerce = new Coerce([new Field('big_id', new Int64())])
    const result = coerce.coerceRow({ big_id: 12345678901234n })
    expect(result).toEqual({ big_id: 12345678901234n })
  })

  it('converts UTC timestamp fields to ISO strings', () => {
    const coerce = new Coerce([new Field('created_at', new TimestampMillisecond('UTC'))])
    const millis = Date.UTC(2024, 0, 15, 10, 30, 0)
    const result = coerce.coerceRow({ created_at: millis })
    expect(result).toEqual({ created_at: new Date(millis).toISOString() })
  })

  it('converts timezone-less (local) timestamp fields to ISO strings', () => {
    const coerce = new Coerce([new Field('created_at', new TimestampMillisecond(null))])
    const millis = Date.UTC(2024, 0, 15, 10, 30, 0)
    const result = coerce.coerceRow({ created_at: millis })
    expect(result).toEqual({ created_at: new Date(millis).toISOString() })
  })

  it('leaves timestamp fields with a non-UTC timezone unchanged', () => {
    const coerce = new Coerce([
      new Field('created_at', new TimestampMillisecond('America/New_York')),
    ])
    const millis = Date.UTC(2024, 0, 15, 10, 30, 0)
    const result = coerce.coerceRow({ created_at: millis })
    expect(result).toEqual({ created_at: millis })
  })

  it('leaves falsy timestamp values untouched', () => {
    const coerce = new Coerce([new Field('created_at', new TimestampMillisecond('UTC'))])
    expect(coerce.coerceRow({ created_at: 0 })).toEqual({ created_at: 0 })
    expect(coerce.coerceRow({ created_at: null })).toEqual({ created_at: null })
  })

  it('handles multiple mixed fields on the same row', () => {
    const coerce = new Coerce([
      new Field('name', new Utf8()),
      new Field('score', new Float64()),
      new Field('created_at', new TimestampMillisecond('UTC')),
    ])
    const millis = Date.UTC(2024, 0, 15, 10, 30, 0)
    const result = coerce.coerceRow({
      name: 'foo',
      score: '3.14',
      created_at: millis,
      ignored: true,
    })
    expect(result).toEqual({
      name: 'foo',
      score: 3.14,
      created_at: new Date(millis).toISOString(),
    })
  })
})
