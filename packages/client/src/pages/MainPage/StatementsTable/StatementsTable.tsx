import React, { useMemo, useState } from "react";
import { useTable, Cell, Row, useExpanded } from "react-table";
import classNames from "classnames";
import { FaInfo, FaPencilAlt, FaTrashAlt, FaClone } from "react-icons/fa";

import { Tag, Button, Submit, Toast } from "components";
import { Entities } from "types";
import { ResponseMetaI, ActantI } from "@shared/types";
import { deleteActant } from "api/deleteActant";
import { toast } from "react-toastify";
import { useHistory, useParams } from "react-router-dom";

interface StatementsTableProps {
  statements: {}[];
  meta: ResponseMetaI;
  actants: ActantI[];
  activeStatementId: string;
  setActiveStatementId: (id: string) => void;
  fetchTerritory: (id: string) => void;
}

interface IActant {
  actant: string;
  certainty: string;
  elvl: string;
  position: string;
}

// FIXME: I had to retype ActantI, because there is not type attribute on ActantI type in @shared
interface ActantITable extends ActantI {
  data: {
    label: string;
    content: string;
    language: string;
    parent: string | false;
    type: string;
  };
}

export const StatementsTable: React.FC<StatementsTableProps> = ({
  statements,
  meta,
  actants,
  setActiveStatementId,
  activeStatementId,
  fetchTerritory,
}) => {
  const history = useHistory();
  const [showSubmit, setShowSubmit] = useState(false);
  const [actantId, setActantId] = useState("");
  const [currentTerritoryId, setCurrentTerritoryId] = useState("");
  const { territoryId } = useParams<{
    territoryId: string;
    statementId: string;
  }>();

  const wrapperClasses = classNames("table-wrapper", "px-1");
  const tableClasses = classNames(
    "component",
    "table",
    "w-full",
    "table-auto",
    "text-sm"
  );

  const columns = useMemo(
    () => [
      {
        Header: "ID",
        accessor: "id",
      },
      {
        Header: "Subjects",
        accessor: "data",
        Cell: ({ row }: Cell) => {
          const subjects =
            row.values.data && row.values.data.actants
              ? row.values.data.actants.filter(
                  (a: IActant) => a.position === "s"
                )
              : [];

          return (
            <div className="table-subjects">
              {subjects.length
                ? subjects.map((actant: IActant, si: number) => {
                    const subjectObject =
                      actants &&
                      (actants.find(
                        (a) => a.id === actant.actant
                      ) as ActantITable);
                    const entity = Entities[subjectObject?.class];
                    return subjectObject && entity ? (
                      <Tag
                        key={si}
                        propId={actant.actant}
                        category={entity.id}
                        color={entity.color}
                        marginRight
                      />
                    ) : null;
                  })
                : null}
            </div>
          );
        },
      },
      {
        Header: "Type",
        accessor: "data.action",
        Cell: ({ row }: Cell) => {
          const actionTypeLabel =
            meta &&
            meta.actions &&
            meta.actions.find((action) => action.id === row.values.data.action)
              ?.labels[0].label;
          return (
            <p>
              {actionTypeLabel && actionTypeLabel.length > 40
                ? `${actionTypeLabel.substring(0, 40)}...`
                : actionTypeLabel}
            </p>
          );
        },
      },
      {
        Header: "Actants",
        Cell: ({ row }: Cell) => {
          const rowActants =
            row.values.data && row.values.data.actants
              ? row.values.data.actants.filter(
                  (a: IActant) => a.position !== "s"
                )
              : [];
          const isOversized = rowActants.length > 4;
          const rowActantsSlice = rowActants.slice(0, 4);

          return (
            <div className="table-subjects inline-flex">
              {rowActantsSlice.length > 0
                ? rowActantsSlice.map((actant: IActant, si: number) => {
                    const actantObject =
                      actants &&
                      (actants.find(
                        (a) => a.id === actant.actant
                      ) as ActantITable);
                    const entity = Entities[actantObject?.class];
                    return actantObject && entity ? (
                      <Tag
                        key={si}
                        propId={actantObject && actantObject.id}
                        category={entity.id}
                        color={entity.color}
                        marginRight
                      />
                    ) : (
                      <div key={si} />
                    );
                  })
                : null}
              {isOversized && <div className="flex items-end">{"..."}</div>}
            </div>
          );
        },
      },
      {
        Header: "",
        id: "expander",
        Cell: ({ row }: Cell) => (
          <div className="table-actions inline-flex float-right">
            <span {...row.getToggleRowExpandedProps()}>
              <Button
                key="i"
                icon={<FaInfo size={14} />}
                color="info"
                onClick={() => (row.isExpanded = !row.isExpanded)}
              />
            </span>
            <Button key="d" icon={<FaClone size={14} />} color="success" />
            <Button
              key="e"
              icon={<FaPencilAlt size={14} />}
              color="warning"
              onClick={() => {
                activeStatementId === row.values.id
                  ? setActiveStatementId("")
                  : setActiveStatementId(row.values.id);
                activeStatementId === row.values.id
                  ? history.push(`/${territoryId}`)
                  : history.push(`/${territoryId}/${row.values.id}`);
              }}
            />
            <Button
              key="r"
              icon={<FaTrashAlt size={14} />}
              color="danger"
              onClick={() => {
                // const territoryId = row.values.data.territory;
                setCurrentTerritoryId(row.values.data.territory);
                setActantId(row.values.id);
                setShowSubmit(true);
              }}
            />
          </div>
        ),
      },
    ],
    [activeStatementId, statements]
  );

  const renderRowSubComponent = React.useCallback(
    ({ row }) => (
      <pre
        style={{
          fontSize: "10px",
          maxWidth: "100px",
        }}
        className={"break-words"}
      >
        <code>{JSON.stringify({ values: row.values }, null, 2)}</code>
      </pre>
    ),
    []
  );

  const {
    getTableProps,
    getTableBodyProps,
    headerGroups,
    rows,
    prepareRow,
    visibleColumns,
  } = useTable(
    {
      columns,
      data: statements,
      initialState: {
        hiddenColumns: ["id"],
      },
    },
    useExpanded
  );

  return (
    <>
      <div className={wrapperClasses}>
        <table {...getTableProps()} className={tableClasses}>
          <thead className="border-b-2 border-black">
            {headerGroups.map((headerGroup, key) => (
              <tr
                {...headerGroup.getHeaderGroupProps()}
                key={key}
                style={{ fontSize: "1rem" }}
              >
                {headerGroup.headers.map((column, key) => (
                  <th
                    className="table-header text-left"
                    {...column.getHeaderProps()}
                    key={key}
                  >
                    {column.render("Header")}
                  </th>
                ))}
              </tr>
            ))}
          </thead>
          <tbody {...getTableBodyProps()}>
            {rows.map((row, i) => {
              prepareRow(row);
              return (
                <React.Fragment key={i}>
                  <tr
                    {...row.getRowProps()}
                    className={classNames({
                      "bg-white": i % 2 == 0,
                      "odd-strip":
                        i % 2 == 1 && row.values.id !== activeStatementId,
                      "bg-primary text-white":
                        row.values.id === activeStatementId,
                    })}
                  >
                    {row.cells.map((cell, i) => {
                      return (
                        <td className="p-1" {...cell.getCellProps()}>
                          {cell.render("Cell")}
                        </td>
                      );
                    })}
                  </tr>
                  {row.isExpanded ? (
                    <tr>
                      <td colSpan={visibleColumns.length}>
                        {renderRowSubComponent({ row })}
                      </td>
                    </tr>
                  ) : null}
                </React.Fragment>
              );
            })}
          </tbody>
        </table>
      </div>
      <Submit
        title={"Delete actant"}
        text={`Do you really want to delete actant with ID [${actantId}]?`}
        show={showSubmit}
        onCancel={() => setShowSubmit(false)}
        onSubmit={() => {
          deleteActant(actantId).then(() => toast.dark("Statement deleted!"));
          setActantId("");
          setActiveStatementId("");
          fetchTerritory(currentTerritoryId);
          setShowSubmit(false);
        }}
      />
      <Toast />
    </>
  );
};