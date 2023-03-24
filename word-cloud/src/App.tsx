import { useEffect, useState } from "react";
import reactLogo from "./assets/react.svg";
import viteLogo from "/vite.svg";
import "./App.css";
import WordCloud from "./components/WordCloud";

const option = {
  series: [
    {
      type: "wordCloud",
      shape: "circle",
      sizeRange: [10, 30],
      rotationRange: [-90, 90],
      rotationStep: 45,
      gridSize: 10,
      drawOutOfBound: false,
      textStyle: {
        normal: {
          fontFamily: "sans-serif",
          fontWeight: "bold",
          color: function () {
            return (
              "rgb(" +
              [
                Math.round(Math.random() * 160),
                Math.round(Math.random() * 160),
                Math.round(Math.random() * 160),
              ].join(",") +
              ")"
            );
          },
        },
      },
      // increase maxSize and reduce minSize to allow for more word sizes
      maxSize: 100,
      minSize: 5,
      data: [],
    },
  ],
};

function App() {
  const [words, setWords] = useState();

  useEffect(() => {
    const fetchData = () => {
      fetch("http://localhost:8000/api/v1/wordcloud")
        .then((response) => response.json())
        .then((data) => {
          setWords(
            data.map((d: any) => {
              return {
                value: d[0] + Math.floor(Math.random() * 100 + 1),
                text: d[1],
              };
            })
          );
        })
        .catch((error) => console.log(error));
    };

    fetchData();
  }, []);

  return (
    <div className="App">
      {words && <WordCloud words={words} />}
      <div>
        <a href="https://vitejs.dev" target="_blank">
          <img src={viteLogo} className="logo" alt="Vite logo" />
        </a>
        <a href="https://reactjs.org" target="_blank">
          <img src={reactLogo} className="logo react" alt="React logo" />
        </a>
      </div>
      <h1>Vite + React</h1>
      <div className="card">
        <p>
          Edit <code>src/App.tsx</code> and save to test HMR
        </p>
      </div>
      <p className="read-the-docs">
        Click on the Vite and React logos to learn more
      </p>
    </div>
  );
}

export default App;
