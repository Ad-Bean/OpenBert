fetch("http://127.0.0.1:31112/function/hello-world-python", {
  method: "POST",
  body: '{"name": "John", "age": 30, "email": "john@example.com"}',
})
  .then((res) => res.text())
  .then((res) => console.log(res));
