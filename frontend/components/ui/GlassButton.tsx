import React from 'react';

interface GlassButtonProps {
  children: React.ReactNode;
  onClick?: () => void;
  type?: 'button' | 'submit' | 'reset';
  disabled?: boolean;
  className?: string;
  variant?: 'primary' | 'secondary';
}

export default function GlassButton({
  children,
  onClick,
  type = 'button',
  disabled = false,
  className = '',
  variant = 'primary',
}: GlassButtonProps) {
  return (
    <button
      type={type}
      onClick={onClick}
      disabled={disabled}
      className={`glass-button ${className} ${
        variant === 'secondary' ? 'bg-opacity-20' : ''
      }`}
    >
      {children}
    </button>
  );
}
