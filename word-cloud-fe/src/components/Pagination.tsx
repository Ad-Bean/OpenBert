import React, { Dispatch, SetStateAction } from "react";

type Props = {
  current: number;
  total: number;
  setPage: Dispatch<SetStateAction<number>>;
};

function Pagination({ current, total, setPage }: Props) {
  const pages = Array.from({ length: total }, (_, index) => index + 1);

  return (
    <ol className="fixed left-0 bottom-10 mx-auto w-full flex justify-center gap-1 text-xs font-medium">
      <li>
        <a
          onClick={() => {
            if (current > 1) setPage(current - 1);
          }}
          className="inline-flex h-8 w-8 items-center justify-center rounded border border-gray-100 cursor-pointer"
        >
          <span className="sr-only">Prev Page</span>
          <svg
            xmlns="http://www.w3.org/2000/svg"
            className="h-3 w-3"
            viewBox="0 0 20 20"
            fill="currentColor"
          >
            <path
              fillRule="evenodd"
              d="M12.707 5.293a1 1 0 010 1.414L9.414 10l3.293 3.293a1 1 0 01-1.414 1.414l-4-4a1 1 0 010-1.414l4-4a1 1 0 011.414 0z"
              clipRule="evenodd"
            />
          </svg>
        </a>
      </li>

      {pages.map((p) => (
        <li>
          <a
            onClick={() => setPage(p)}
            className={`block h-8 w-8 rounded text-center leading-8 cursor-pointer ${
              current === p
                ? "border-blue-600 bg-blue-600 text-white"
                : "border border-gray-100 "
            } `}
          >
            {p}
          </a>
        </li>
      ))}

      <li>
        <a
          onClick={() => setPage(current + 1)}
          className="inline-flex h-8 w-8 items-center justify-center rounded border border-gray-100 cursor-pointer"
        >
          <span className="sr-only">Next Page</span>
          <svg
            xmlns="http://www.w3.org/2000/svg"
            className="h-3 w-3"
            viewBox="0 0 20 20"
            fill="currentColor"
          >
            <path
              fillRule="evenodd"
              d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z"
              clipRule="evenodd"
            />
          </svg>
        </a>
      </li>
    </ol>
  );
}

export default Pagination;
