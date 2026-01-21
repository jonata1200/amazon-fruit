/**
 * Exports Centralizados - Componentes UI
 * Exporta todos os componentes UI do design system
 */

// Componentes Base
export { Button, type ButtonProps } from './button';
export { Input, type InputProps } from './input';
export { 
  Card, 
  CardHeader, 
  CardTitle, 
  CardDescription, 
  CardContent, 
  CardFooter,
  type CardProps 
} from './card';
export { Label, type LabelProps } from './label';

// Componentes de Feedback
export { Skeleton, type SkeletonProps } from './skeleton';
export { Spinner, type SpinnerProps } from './spinner';
export { Progress, type ProgressProps } from './progress';
export { LoadingScreen } from './loading-screen';

// Componentes de Overlay
export { 
  Dialog, 
  DialogTrigger, 
  DialogContent, 
  DialogHeader, 
  DialogTitle, 
  DialogDescription, 
  DialogFooter,
  type DialogContentProps 
} from './dialog';
export { 
  DropdownMenu, 
  DropdownMenuTrigger, 
  DropdownMenuContent, 
  DropdownMenuItem,
  type DropdownMenuContentProps,
  type DropdownMenuItemProps 
} from './dropdown-menu';
export { Tooltip, type TooltipProps } from './tooltip';

// Componentes de Dados
export { DataTable, type DataTableProps, type Column } from './data-table';
export { EmptyState, type EmptyStateProps } from './empty-state';

// Componentes Auxiliares
export { Icon } from './icon';
export { Toaster } from './toaster';

// Skeletons Específicos
export { ChartSkeleton } from './skeletons/chart-skeleton';
export { KPISkeleton } from './skeletons/kpi-skeleton';
export { TableSkeleton } from './skeletons/table-skeleton';
