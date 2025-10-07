import React from 'react';

interface GlassButtonProps {
  children: React.ReactNode;
  onClick?: () => void;
  type?: 'button' | 'submit' | 'reset';
  disabled?: boolean;
  className?: string;
  variant?: 'primary' | 'secondary';
  fullWidth?: boolean;
  size?: 'small' | 'medium' | 'large';
}

export default function GlassButton({
  children,
  onClick,
  type = 'button',
  disabled = false,
  className = '',
  variant = 'primary',
  fullWidth = false,
  size = 'medium',
}: GlassButtonProps) {
  const sizeClasses = {
    small: '!px-4 !py-2 text-sm',
    medium: '!px-6 !py-3 text-base',
    large: '!px-8 !py-4 text-lg',
  };

  return (
    <button
      type={type}
      onClick={onClick}
      disabled={disabled}
      className={`glass-button ${sizeClasses[size]} ${fullWidth ? 'w-full' : ''} ${className} ${
        variant === 'secondary' ? 'bg-opacity-20' : ''
      }`}
    >
      {children}
    </button>
  );
}
