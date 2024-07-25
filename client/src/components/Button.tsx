import * as React from "react";

export interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  asChild?: boolean;
  onAsyncClick?: () => Promise<void | (() => void)>;
  full?: boolean;
  text: string;
}

const Button = ({ onAsyncClick, full, text, ...props }: ButtonProps) => {
  const [actionInProgress, setActionInProgress] = React.useState(false);

  const handleAsyncOnPress = async () => {
    setActionInProgress(true);

    const unmountCallback = await onAsyncClick!();
    if (unmountCallback) {
      unmountCallback();
    } else {
      setActionInProgress(false);
    }
  };

  const handler = onAsyncClick
    ? async () => {
        await handleAsyncOnPress();
      }
    : props.onClick;

  return (
    <button
      className={`${""} bg-gradient-to-t from-sky-700 to-sky-500 text-white font-bold py-2 px-4 hover:scale-105
      flex rounded-md cursor-pointer outline-none focus:outline-none transition-all duration-200`}
      type="button"
      onClick={handler}
      {...props}
    >
      <span>{text}</span>
      {actionInProgress && <div className="ml-4 font-bold animate-spin">c</div>}
    </button>
  );
};

Button.displayName = "Button";

export { Button };
