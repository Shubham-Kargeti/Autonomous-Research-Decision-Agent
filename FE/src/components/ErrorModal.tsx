import "./styles/ErrorModal.css";

interface Props {
  message?: string;
  onRetry: () => void;
  onClose: () => void;
}

function ErrorModal({
  message = "Our AI tried to think too hard and crashed 😅",
  onRetry,
  onClose,
}: Props) {
  return (
    <div className="error-overlay">
      <div className="error-box">
        <div className="error-emoji">🤖💥</div>

        <h3>Oops! Something went wrong</h3>

        <p className="error-message">{message}</p>

        <div className="error-actions">
          <button className="retry-btn" onClick={onRetry}>
            Try Again
          </button>

          <button className="close-btn" onClick={onClose}>
            Close
          </button>
        </div>
      </div>
    </div>
  );
}

export default ErrorModal;
