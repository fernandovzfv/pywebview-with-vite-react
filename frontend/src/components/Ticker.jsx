import { useState, useEffect } from "react";
import { Text } from "@radix-ui/themes";

export default function Ticker() {
  const [ticker, setTicker] = useState("");

  useEffect(() => {
    const handlePywebviewReady = () => {
      if (!window.pywebview.state) {
        window.pywebview.state = {};
      }

      // @ts-expect-error This is a custom state
      window.pywebview.state.setTicker = setTicker;
    };

    if (window.pywebview) {
      handlePywebviewReady();
    } else {
      window.addEventListener("pywebviewready", handlePywebviewReady);
    }

    return () => {
      window.removeEventListener("pywebviewready", handlePywebviewReady);
    };
  }, []);

  return (
    <Text
      size="5"
      weight="bold"
      style={{
        fontFamily: "'Digital-7', monospace",
        letterSpacing: "0.1em",
        color: "#00ff00",
        textShadow: "0 0 10px #00ff00",
      }}
    >
      {ticker}
    </Text>
  );
}
