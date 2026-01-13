// src/lib/utils/validators.ts

export const isValidDate = (date: string): boolean => {
  const regex = /^\d{4}-\d{2}-\d{2}$/;
  if (!regex.test(date)) return false;

  const d = new Date(date);
  return d instanceof Date && !isNaN(d.getTime());
};

export const isValidDateRange = (start: string, end: string): boolean => {
  if (!isValidDate(start) || !isValidDate(end)) return false;

  const startDate = new Date(start);
  const endDate = new Date(end);

  return startDate <= endDate;
};

export const isValidEmail = (email: string): boolean => {
  const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return regex.test(email);
};
