import { resolve } from "path";
import * as TJS from "typescript-json-schema";

// optionally pass argument to schema generator
const settings: TJS.PartialArgs = {
    required: true,
};

// optionally pass ts compiler options
const compilerOptions: TJS.CompilerOptions = {
    strictNullChecks: true,
};

// optionally pass a base path
const basePath = "./";

const program = TJS.getProgramFromFiles(
  [resolve("parse.ts")],
  compilerOptions,
  basePath
);

// We can either get the schema for one file and one type...
const schema = TJS.generateSchema(program, "IStatement", settings);

// ... or a generator that lets us incrementally get more schemas

const generator  = TJS.buildGenerator(program, settings);

// generator can be also reused to speed up generating the schema if usecase allows:
const schemaWithReusedGenerator = TJS.generateSchema(program, "IStatement", settings, [], generator);

// all symbols
const symbols = generator.getUserSymbols();

// Get symbols for different types from generator.
//generator.getSchemaForSymbol("MyType");
//generator.getSchemaForSymbol("AnotherType");