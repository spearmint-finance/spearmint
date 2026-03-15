import { useState, useCallback } from 'react';
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  Box,
  Typography,
  Alert,
  CircularProgress,
  List,
  ListItemButton,
  ListItemIcon,
  ListItemText,
} from '@mui/material';
import {
  AccountBalance as BankIcon,
  ShowChart as InvestmentIcon,
} from '@mui/icons-material';
import { usePlaidLink } from 'react-plaid-link';
import { useMutation, useQuery } from '@tanstack/react-query';
import {
  createPlaidLinkToken,
  exchangePlaidToken,
  getAkoyaAuthUrl,
} from '../../api/aggregator';

interface LinkAccountDialogProps {
  open: boolean;
  onClose: () => void;
  onAccountLinked: () => void;
}

function PlaidLinkFlow({
  onSuccess,
  onClose,
}: {
  onSuccess: () => void;
  onClose: () => void;
}) {
  const { data: linkTokenData, isLoading: tokenLoading, error: tokenError } = useQuery({
    queryKey: ['plaidLinkToken'],
    queryFn: createPlaidLinkToken,
    refetchOnWindowFocus: false,
    retry: false,
  });

  const exchangeMutation = useMutation({
    mutationFn: (params: { publicToken: string; institutionId?: string; institutionName?: string }) =>
      exchangePlaidToken(params.publicToken, params.institutionId, params.institutionName),
    onSuccess: () => {
      onSuccess();
      onClose();
    },
  });

  const onPlaidSuccess = useCallback(
    (publicToken: string, metadata: any) => {
      exchangeMutation.mutate({
        publicToken,
        institutionId: metadata?.institution?.institution_id,
        institutionName: metadata?.institution?.name,
      });
    },
    [exchangeMutation],
  );

  const { open: openPlaid, ready } = usePlaidLink({
    token: linkTokenData?.link_token ?? null,
    onSuccess: onPlaidSuccess,
  });

  if (tokenLoading) {
    return (
      <Box textAlign="center" py={3}>
        <CircularProgress size={24} />
        <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
          Preparing secure connection...
        </Typography>
      </Box>
    );
  }

  if (tokenError) {
    return (
      <Alert severity="error">
        Plaid is not configured. Set PLAID_CLIENT_ID and PLAID_SECRET in your environment.
      </Alert>
    );
  }

  return (
    <Box textAlign="center" py={2}>
      {exchangeMutation.isError && (
        <Alert severity="error" sx={{ mb: 2 }}>
          Failed to link account. Please try again.
        </Alert>
      )}
      <Button
        variant="contained"
        size="large"
        onClick={() => openPlaid()}
        disabled={!ready || exchangeMutation.isPending}
      >
        {exchangeMutation.isPending ? 'Linking...' : 'Connect Your Bank'}
      </Button>
      <Typography variant="caption" display="block" color="text.secondary" sx={{ mt: 1 }}>
        Securely connect via Plaid. Your credentials are never shared with Spearmint.
      </Typography>
    </Box>
  );
}

export default function LinkAccountDialog({
  open,
  onClose,
  onAccountLinked,
}: LinkAccountDialogProps) {
  const [selectedProvider, setSelectedProvider] = useState<'plaid' | 'akoya' | null>(null);

  const akoyaMutation = useMutation({
    mutationFn: () => getAkoyaAuthUrl('fidelity'),
    onSuccess: (data) => {
      // Redirect to Akoya OAuth
      window.location.href = data.authorization_url;
    },
  });

  const handleClose = () => {
    setSelectedProvider(null);
    onClose();
  };

  return (
    <Dialog open={open} onClose={handleClose} maxWidth="sm" fullWidth>
      <DialogTitle>Link Bank Account</DialogTitle>
      <DialogContent>
        {!selectedProvider && (
          <>
            <Typography variant="body2" color="text.secondary" gutterBottom>
              Connect your bank to automatically sync transactions, balances, and holdings.
            </Typography>
            <List sx={{ mt: 1 }}>
              <ListItemButton
                onClick={() => setSelectedProvider('plaid')}
                sx={{ border: 1, borderColor: 'divider', borderRadius: 1, mb: 1 }}
              >
                <ListItemIcon>
                  <BankIcon color="primary" />
                </ListItemIcon>
                <ListItemText
                  primary="Connect a Bank"
                  secondary="Chase, Bank of America, Wells Fargo, Capital One, and 12,000+ others"
                />
              </ListItemButton>
              <ListItemButton
                onClick={() => {
                  setSelectedProvider('akoya');
                  akoyaMutation.mutate();
                }}
                disabled={akoyaMutation.isPending}
                sx={{ border: 1, borderColor: 'divider', borderRadius: 1 }}
              >
                <ListItemIcon>
                  <InvestmentIcon color="success" />
                </ListItemIcon>
                <ListItemText
                  primary="Connect Fidelity"
                  secondary="Fidelity brokerage, 401k, IRA, and cash management accounts"
                />
                {akoyaMutation.isPending && <CircularProgress size={20} />}
              </ListItemButton>
            </List>
            {akoyaMutation.isError && (
              <Alert severity="error" sx={{ mt: 1 }}>
                Akoya is not configured. Set AKOYA_CLIENT_ID and AKOYA_CLIENT_SECRET.
              </Alert>
            )}
          </>
        )}

        {selectedProvider === 'plaid' && (
          <PlaidLinkFlow onSuccess={onAccountLinked} onClose={handleClose} />
        )}

        {selectedProvider === 'akoya' && (
          <Box textAlign="center" py={3}>
            <CircularProgress size={24} />
            <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
              Redirecting to Fidelity for authorization...
            </Typography>
          </Box>
        )}
      </DialogContent>
      <DialogActions>
        {selectedProvider === 'plaid' ? (
          <Button onClick={() => setSelectedProvider(null)}>Back</Button>
        ) : (
          <Button onClick={handleClose}>Cancel</Button>
        )}
      </DialogActions>
    </Dialog>
  );
}
