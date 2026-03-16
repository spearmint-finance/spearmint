import { Alert, AlertTitle, Button } from '@mui/material';
import type { LinkedProvider } from '../../types/aggregator';

interface ReconnectBannerProps {
  providers: LinkedProvider[];
  onReconnect: (provider: LinkedProvider) => void;
}

export default function ReconnectBanner({ providers, onReconnect }: ReconnectBannerProps) {
  const needsAttention = providers.filter((p) => p.status === 'login_required');

  if (needsAttention.length === 0) return null;

  return (
    <>
      {needsAttention.map((provider) => (
        <Alert
          key={provider.id}
          severity="warning"
          sx={{ mb: 2 }}
          action={
            <Button color="inherit" size="small" onClick={() => onReconnect(provider)}>
              Reconnect
            </Button>
          }
        >
          <AlertTitle>Connection needs attention</AlertTitle>
          Your {provider.institution_name || 'bank'} connection requires re-authentication.
          {provider.error_message && ` ${provider.error_message}`}
        </Alert>
      ))}
    </>
  );
}
