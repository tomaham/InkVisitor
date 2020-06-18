import {Request, Response, Router} from 'express';
import {BAD_REQUEST, CREATED, OK} from 'http-status-codes';
import { v4 as uuid4} from 'uuid';

import { paramMissingError } from '@shared/constants';
import { stat } from 'fs';

class Statement {
    public id : string;
    public tree: object;

    constructor(id: string, tree: object) {
        this.id = id;
        this.tree = tree;
    }
}

interface Repository<T> {
    saveOne(entity: T) : Promise<void>;
    findAll() : Promise<T[]>;
    findOne(id: string) : Promise<T | undefined>;
}

interface IStatementRepository extends Repository<Statement> {
}

/**
 * The statement entity repository.
 */
class StatementRepository implements IStatementRepository {

    // Mockups
    private statements = [
        new Statement('11111111-1111-1111-1111-111111111111', {}),
        new Statement('22222222-2222-2222-2222-222222222222', {}),
        new Statement('33333333-3333-3333-3333-333333333333', {}),
    ]

    async saveOne(statement: Statement) :Promise<void> { 
        // if statement in statements raise exception.
        this.statements.push(statement);
    }

    /**
     * Get the all statements.
     */
    async findAll() : Promise<Statement[]> {
        return [...this.statements];
    }
    
    /**
     * Get the one statement.
     * @param id 
     */
    async findOne(statement_id: string /*UUID*/ ) : Promise<Statement | undefined> {
        return this.statements.find( ({id}) => id === statement_id);
    }
}

const router = Router()
const repository = new StatementRepository() 

/**  
 * Get the statements `GET /api/statements`.
 */
router.get("/", async (request: Request, response: Response) => {
    const statements = await repository.findAll();
    return response.status(OK).json(statements);
})

/** 
 *  Get the statement `GET /api/statements/:id`. 
 */
router.get("/:uuid", async (request: Request, response: Response) => {
    const uuid = request.params.uuid;
    const statement = await repository.findOne(uuid);
    return response.status(OK).json(statement);
})

// Create the statement `POST /api/statement/`.
router.post('/', async (request: Request, response: Response) => {

    const { statement } = request.body;
    
    if (!statement) {
        return response.status(BAD_REQUEST).json({
            error: paramMissingError,
        });
    }

    await repository.saveOne(statement);

    return response.status(CREATED).end();
});

export default router;