import { Box, Alert, AlertTitle, Button } from '@mui/material'
import RefreshIcon from '@mui/icons-material/Refresh'

interface ErrorDisplayProps {
  message?: string
  title?: string
  onRetry?: () => void
}

function ErrorDisplay({
  message = 'An error occurred while loading data.',
  title = 'Error',
  onRetry,
}: ErrorDisplayProps) {
  return (
    <Box sx={{ p: 2 }}>
      <Alert
        severity="error"
        action={
          onRetry && (
            <Button
              color="inherit"
              size="small"
              startIcon={<RefreshIcon />}
              onClick={onRetry}
            >
              Retry
            </Button>
          )
        }
      >
        <AlertTitle>{title}</AlertTitle>
        {message}
      </Alert>
    </Box>
  )
}

export default ErrorDisplay

