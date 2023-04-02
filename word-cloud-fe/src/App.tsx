import { useEffect, useState } from "react";
import WordCloud from "./components/WordCloud";
import BlogPosts from "./components/BlogPosts";
import Loading from "./components/Loading";
import { WordCloudOptions, WordCloudType } from "./types/WordCloud";
import { Blog } from "./types/Blog";
import Pagination from "./components/Pagination";

function App() {
  const [words, setWords] = useState<WordCloudOptions[]>();
  const [blogs, setBlogs] = useState<Blog[]>();
  const [page, setPage] = useState(1);
  const pageSize = 3;

  const fetchData = () => {
    fetch("https://hnstream.herokuapp.com/api/v1/wordcloud")
      .then((response) => response.json())
      .then((data: WordCloudType[]) =>
        setWords(
          data.map((d) => ({
            value: d[0] + Math.floor(Math.random() * 100 + 20),
            text: d[1],
          }))
        )
      )
      .catch((error) => console.log(error));
  };

  const fetchPosts = (page: number, pageSize: number) => {
    fetch(
      `https://hnstream.herokuapp.com/api/v1/posts?page_number=${page}&page_size=${pageSize}`
    )
      .then((response) => response.json())
      .then((posts: Blog[]) => {
        setBlogs(posts);
      })
      .catch((error) => console.log(error));
  };

  useEffect(() => {
    fetchPosts(page, pageSize);
  }, [page]);

  useEffect(() => {
    const intervalId = setInterval(() => {
      fetchData();
    }, 10000);
    return () => clearInterval(intervalId);
  }, []);

  return (
    <div className="mx-auto max-w-5xl">
      {words ? <WordCloud words={words} /> : <Loading />}

      <BlogPosts blogs={blogs} />

      <Pagination current={page} total={10} setPage={setPage} />
    </div>
  );
}

export default App;
