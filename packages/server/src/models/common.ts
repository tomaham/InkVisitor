export type UnknownObject = Record<string, unknown> | undefined;

export interface IModel {
  isValid(): boolean; // validate model before inserting to the db
}

export function fillFlatObject<T>(
  ctx: T,
  source: Record<string, unknown> | null
): void {
  if (!source) {
    return;
  }
  for (const key of Object.keys(source)) {
    const wantedType = typeof (ctx as Record<string, unknown>)[key];
    if (wantedType === "object") {
      // only flat object's props
      continue;
    }

    const gotType = typeof source[key];
    if (wantedType !== gotType) {
      throw new Error(
        `cannot parse key ${key}(wants ${wantedType}, got ${gotType})`
      );
    }

    (ctx as Record<string, unknown>)[key] = source[key];
  }
}

type AConstructorTypeOf<T> = new (...data: any[]) => T;

export function fillArray<T>(
  ctx: T[],
  constructor: AConstructorTypeOf<T>,
  source: unknown[] | unknown
): void {
  if (!source) {
    return;
  }
  for (const sourceElement of source as unknown[]) {
    ctx.push(new constructor(sourceElement));
  }
}
