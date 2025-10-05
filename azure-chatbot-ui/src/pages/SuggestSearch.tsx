import { useState } from "react";
import { Form, Button, ListGroup, Spinner, Alert } from "react-bootstrap";
import { useSuggestSearch } from "../hooks/DocumentHook";

const SuggestSearch = () => {
  const [query, setQuery] = useState("");
  const [submitted, setSubmitted] = useState("");

  const { data, status, isFetching } = useSuggestSearch(
    submitted,
    10,
    submitted !== "",
  );

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    setSubmitted(query);
  };

  return (
    <div className="container my-5">
      <h1 className="fw-bold text-warning text-center">Suggest Search</h1>

      <Form className="d-flex my-4" onSubmit={handleSearch}>
        <Form.Control
          type="text"
          placeholder="Type to get suggestions..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          className="me-2"
        />
        <Button type="submit" variant="warning">
          Search
        </Button>
      </Form>

      {isFetching && (
        <div className="text-center my-3">
          <Spinner animation="border" />
        </div>
      )}

       {status === "error" && (
        <Alert variant="danger">
          Error fetching suggestions:
        </Alert>
      )}

      {status === "success" && data && (
        <ListGroup>
          {data.length > 0 ? (
            data.map((suggestion: string, idx: number) => (
              <ListGroup.Item key={idx}>{suggestion}</ListGroup.Item>
            ))
          ) : (
            <ListGroup.Item>No suggestions found</ListGroup.Item>
          )}
        </ListGroup>
      )}
    </div>
  );
};

export default SuggestSearch;
