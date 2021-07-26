import { IActant, IStatement } from "@shared/types";

export const findPositionInStatement = (
  statement: IStatement,
  actant: IActant
) => {
  if (
    statement.data.actants
      .filter((a) => a.position === "s")
      .find((a) => a.actant === actant.id)
  ) {
    return "subject";
  } else if (
    statement.data.actants
      .filter((a) => a.position === "a1")
      .find((a) => a.actant === actant.id)
  ) {
    return "actant1";
  } else if (
    statement.data.actants
      .filter((a) => a.position === "a2")
      .find((a) => a.actant === actant.id)
  ) {
    return "actant2";
  } else if (
    statement.data.actants
      .filter((a) => a.position === "p")
      .find((a) => a.actant === actant.id)
  ) {
    return "pseudo-actant";
  } else if (statement.data.tags.find((t) => t === actant.id)) {
    return "tag";
  } else if (statement.data.territory.id === actant.id) {
    return "territory";
  } else if (statement.data.props.find((p) => p.value.id === actant.id)) {
    return "property value";
  } else if (statement.data.props.find((p) => p.type.id === actant.id)) {
    return "property type";
  } else if (statement.data.references.find((r) => r.resource === actant.id)) {
    return "reference";
  }
};

export function debounce<T extends (...args: any[]) => any>(
  callback: T,
  ms: number
): (...args: Parameters<T>) => Promise<ReturnType<T>> {
  let timer: NodeJS.Timeout | undefined;

  return (...args: Parameters<T>) => {
    if (timer) {
      clearTimeout(timer);
    }
    return new Promise<ReturnType<T>>((resolve) => {
      timer = setTimeout(() => {
        const returnValue = callback(...args) as ReturnType<T>;
        resolve(returnValue);
      }, ms);
    });
  };
}