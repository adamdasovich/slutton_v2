import React from 'react';

interface GlassInputProps {
  type?: string;
  placeholder?: string;
  value?: string;
  onChange?: (e: React.ChangeEvent<HTMLInputElement>) => void;
  name?: string;
  required?: boolean;
  className?: string;
}

export default function GlassInput({
  type = 'text',
  placeholder,
  value,
  onChange,
  name,
  required = false,
  className = '',
}: GlassInputProps) {
  return (
    <input
      type={type}
      placeholder={placeholder}
      value={value}
      onChange={onChange}
      name={name}
      required={required}
      className={`glass-input w-full ${className}`}
    />
  );
}
