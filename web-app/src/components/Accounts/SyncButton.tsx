import { IconButton, Tooltip } from '@mui/material';
import { Sync as SyncIcon } from '@mui/icons-material';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { useSnackbar } from 'notistack';
import { syncProvider } from '../../api/aggregator';

interface SyncButtonProps {
  linkedProviderId: number;
}

export default function SyncButton({ linkedProviderId }: SyncButtonProps) {
  const queryClient = useQueryClient();
  const { enqueueSnackbar } = useSnackbar();

  const syncMutation = useMutation({
    mutationFn: () => syncProvider(linkedProviderId),
    onSuccess: (result) => {
      const parts: string[] = [];
      if (result.transactions_added > 0) parts.push(`${result.transactions_added} transactions`);
      if (result.balances_updated > 0) parts.push(`${result.balances_updated} balances`);
      if (result.holdings_updated > 0) parts.push(`${result.holdings_updated} holdings`);
      const msg = parts.length > 0
        ? `Synced: ${parts.join(', ')}`
        : 'Already up to date';
      enqueueSnackbar(msg, { variant: 'success' });

      queryClient.invalidateQueries({ queryKey: ['accounts'] });
      queryClient.invalidateQueries({ queryKey: ['netWorth'] });
      queryClient.invalidateQueries({ queryKey: ['transactions'] });
      queryClient.invalidateQueries({ queryKey: ['linkedProviders'] });
    },
    onError: () => {
      enqueueSnackbar('Sync failed. Please try again.', { variant: 'error' });
    },
  });

  return (
    <Tooltip title="Sync now">
      <IconButton
        size="small"
        aria-label="Sync account data"
        onClick={(e) => {
          e.stopPropagation();
          syncMutation.mutate();
        }}
        disabled={syncMutation.isPending}
        sx={{
          animation: syncMutation.isPending ? 'spin 1s linear infinite' : 'none',
          '@keyframes spin': { '100%': { transform: 'rotate(360deg)' } },
        }}
      >
        <SyncIcon fontSize="small" />
      </IconButton>
    </Tooltip>
  );
}
