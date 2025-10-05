import { useState } from "react";
import { useKeywordSearch } from "../../hooks/DocumentHook";
import { Form, Button, Spinner } from "react-bootstrap";
import type { SearchResult } from "../../types/searchResult";

const Documents = () => {
  const [query, setQuery] = useState("");
  const [submitted, setSubmitted] = useState("");

  const { data, status, isFetching } = useKeywordSearch(
    submitted,
    submitted !== "",
  );

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    setSubmitted(query);
  };

  return (
    <div className="container my-5">
      <h1 className="fw-bold text-primary text-center">Search Documents</h1>

      <Form className="d-flex my-4" onSubmit={handleSearch}>
        <Form.Control
          type="text"
          placeholder="Search documents..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          className="me-2"
        />
        <Button type="submit" variant="success">
          Search
        </Button>
      </Form>

      {isFetching && (
        <div className="text-center my-3">
          <Spinner animation="border" />
        </div>
      )}

      {status === "success" && data && (
        <div className="row row-cols-1 row-cols-md-2 row-cols-lg-3 g-4">
          {data.map((doc: SearchResult, idx: number) => (
            <div key={idx} className="col">
              <div className="card shadow-sm h-100">
                <div className="card-body">
                  <h5 className="card-title text-primary">{doc.fileName}</h5>

                  <ul className="list-unstyled mb-3">
                    <li>
                      <strong>Blob Name:</strong> {doc.fileName}
                    </li>
                    <li>
                      <strong>Blob Path:</strong>{" "}
                      <a
                        href={doc.blobPath}
                        target="_blank"
                        rel="noopener noreferrer"
                      >
                        {doc.blobPath}
                      </a>
                    </li>
                    {doc.description && (
                      <li>
                        <strong>Description:</strong> {doc.description}
                      </li>
                    )}
                  </ul>

                  <p className="card-text">
                    <strong>Content:</strong>{" "}
                    {doc.contentSnippet?.length > 0
                      ? doc.contentSnippet
                      : "No preview available"}
                  </p>
                </div>

                <div className="card-footer bg-transparent border-0">
                  <a
                    href={doc.blobPath}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="btn btn-primary w-100"
                  >
                    Open Document
                  </a>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default Documents;
