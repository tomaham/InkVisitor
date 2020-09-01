import { Connection, r as rethink } from "rethinkdb-ts"
import { Express, NextFunction, Request, Response } from "express"


declare global {
    namespace Express {
        export interface Request {
            rethink: Connection
        }
    }
}

export const rethinkConfig = {
    db: "dissinet",
    host: "localhost",
    port: 28015,
    authKey: ""
};

/**
 * Send back a 500 error.
 */
export function handleErrorMiddleware(response: Response) {
    return (error: any) => {
        const status = 500;
        const message = error.message
        response.send({ status, message });
    }
}

/**
 * Open RethinkDB connection and store in `request.rethink`.
 */
export const createConnection = async (request: Request, response: Response, next: NextFunction) => {
    await rethink.connectPool(rethinkConfig);
    const connection = await rethink.connect(rethinkConfig);
    request.rethink = connection;
}

/*
 * Close the RethinkDB connection stored in `request.rethink`.
 */
export const closeConnection = async (request: Request, response: Response, next: NextFunction) => {
    await request.rethink.close();
}