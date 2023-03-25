import React from "react";
import ReactWordcloud, { OptionsProp } from "react-wordcloud";

type Props = {
  words: any;
};
export default function WordCloud({ words }: Props) {
  const options: OptionsProp = {
    fontSizes: [32, 64],
    rotations: 2,
    rotationAngles: [-90, 0],
  };

  return (
    <div className="mx-auto max-w-5xl">
      <section className="mt-2">
        <ReactWordcloud options={options} words={words} />
      </section>
    </div>
  );
}
