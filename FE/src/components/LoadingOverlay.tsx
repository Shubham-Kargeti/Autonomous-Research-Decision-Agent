import { useEffect, useState } from "react";
import "./styles/LoadingOverlay.css";

const messages = [
  "Agent is thinking...",
  "Summoning AI brain cells 🧠",
  "Consulting the digital universe 🌌",
  "Charging neural circuits ⚡",
  "Convincing the LLM to cooperate 🤖",
];

interface Props {
  message?: string;
}

function LoadingOverlay({ message }: Props) {
  const [dynamicMessage, setDynamicMessage] = useState(messages[0]);

  useEffect(() => {
    const interval = setInterval(() => {
      const random =
        messages[Math.floor(Math.random() * messages.length)];
      setDynamicMessage(random);
    }, 2000);

    return () => clearInterval(interval);
  }, []);

  return (
    <div className="loading-overlay">
      <div className="loading-card">
        <div className="ai-animation">
          <div className="pulse-circle"></div>
          <div className="pulse-circle delay"></div>
          <div className="bolt">⚡</div>
        </div>

        <p className="loading-text">
          {message || dynamicMessage}
        </p>
      </div>
    </div>
  );
}

export default LoadingOverlay;
