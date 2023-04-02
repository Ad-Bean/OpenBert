import React, { useEffect } from "react";
import { Blog } from "../types/Blog";

type Props = {
  blogs: Blog[] | undefined;
};

function BlogPosts({ blogs }: Props) {
  return (
    <div className="app">
      {blogs ? (
        blogs?.map((blog, idx) => <BlogCard key={idx} blog={blog} />)
      ) : (
        <LoadingCard />
      )}
    </div>
  );
}

export default BlogPosts;

type BlogCardPorps = {
  blog: Blog;
};
const BlogCard = ({ blog }: BlogCardPorps) => (
  <article className="rounded-lg border border-gray-100 p-4 shadow-sm transition hover:shadow-lg sm:p-6 my-6 max-w-4xl mx-auto">
    <span className="inline-block rounded bg-blue-600 p-2 text-white">
      <svg
        xmlns="http://www.w3.org/2000/svg"
        className="h-6 w-6"
        fill="none"
        viewBox="0 0 24 24"
        stroke="currentColor"
      >
        <path d="M12 14l9-5-9-5-9 5 9 5z" />
        <path d="M12 14l6.16-3.422a12.083 12.083 0 01.665 6.479A11.952 11.952 0 0012 20.055a11.952 11.952 0 00-6.824-2.998 12.078 12.078 0 01.665-6.479L12 14z" />
        <path
          strokeLinecap="round"
          strokeLinejoin="round"
          strokeWidth="2"
          d="M12 14l9-5-9-5-9 5 9 5zm0 0l6.16-3.422a12.083 12.083 0 01.665 6.479A11.952 11.952 0 0012 20.055a11.952 11.952 0 00-6.824-2.998 12.078 12.078 0 01.665-6.479L12 14zm-4 6v-7.5l4-2.222"
        />
      </svg>
    </span>

    <time dateTime="2022-10-10" className="block text-xs text-gray-500">
      {blog.timestamp}
    </time>

    <a href={blog.url}>
      <h3 className="mt-1 text-lg font-medium text-gray-900">{blog.title}</h3>
    </a>

    <div className="mt-1 -ml-1 flex flex-wrap gap-2">
      {blog.keyphrases.map((key) => (
        <span
          key={key}
          className="whitespace-nowrap rounded-full bg-blue-100 px-2.5 py-0.5 text-xs text-blue-600"
        >
          {key}
        </span>
      ))}
    </div>

    <p className="mt-3 text-sm leading-relaxed text-gray-500 line-clamp-3 h-16">
      {blog.summary}
    </p>

    <a
      href={blog.url}
      className="group mt-4 inline-flex items-center gap-1 text-sm font-medium text-blue-600"
    >
      Find out more
      <span
        aria-hidden="true"
        className="block transition group-hover:translate-x-0.5"
      >
        &rarr;
      </span>
    </a>
  </article>
);

const LoadingCard = () => (
  <article className="rounded-lg border border-gray-100 p-4 shadow-sm transition hover:shadow-lg sm:p-6 max-w-4xl mx-auto">
    <div className="animate-pulse flex space-x-4 rounded-[10px] bg-white p-4 !pt-8 sm:p-6">
      <div className="rounded-full bg-slate-700 h-10 w-10"></div>
      <div className="flex-1 space-y-6 py-1">
        <div className="h-2 bg-slate-700 rounded"></div>
        <div className="space-y-3">
          <div className="grid grid-cols-3 gap-4">
            <div className="h-2 bg-slate-700 rounded col-span-2"></div>
            <div className="h-2 bg-slate-700 rounded col-span-1"></div>
          </div>
          <div className="h-2 bg-slate-700 rounded"></div>
        </div>
      </div>
    </div>
  </article>
);
