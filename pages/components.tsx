import React from 'react';

interface CircularProgressProps {
  progress: number;
  size: number;
}

const CircularProgress: React.FC<CircularProgressProps> = ({ progress, size }) => {
  const strokeWidth = 10;
  const radius = (size - strokeWidth) / 2;
  const circumference = radius * 2 * Math.PI;
  const offset = circumference - (progress / 100) * circumference;
  const textPosition = size / 2;

  return (
    <div className={`relative w-${size} h-${size}`}>
      <svg className="absolute top-0 left-0" width={size} height={size}>
        <circle
          className="stroke-current text-gray-300"
          strokeWidth={strokeWidth}
          fill="transparent"
          r={radius}
          cx={size / 2}
          cy={size / 2}
        />
        <circle
          className="stroke-current text-blue-500"
          strokeWidth={strokeWidth}
          strokeDasharray={circumference}
          strokeDashoffset={offset}
          strokeLinecap="round"
          fill="transparent"
          r={radius}
          cx={size / 2}
          cy={size / 2}
        />
        <text
          x={textPosition}
          y={textPosition + 8} // Adjust vertical positioning of the text
          textAnchor="middle"
          className="text-2xl font-bold text-blue-500"
        >
          {progress}%
        </text>
      </svg>
    </div>
  );
};

export default CircularProgress;
