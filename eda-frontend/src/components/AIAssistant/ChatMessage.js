import React from 'react';
import { Paper, Typography, makeStyles } from '@material-ui/core';

const useStyles = makeStyles((theme) => ({
  messageRow: {
    display: 'flex',
    width: '100%',
    marginBottom: theme.spacing(2),
  },
  userRow: {
    justifyContent: 'flex-end',
  },
  assistantRow: {
    justifyContent: 'flex-start',
  },
  bubble: {
    padding: theme.spacing(1, 2),
    maxWidth: '85%',
    wordBreak: 'break-word',
    whiteSpace: 'pre-wrap',
  },
  userBubble: {
    backgroundColor: theme.palette.primary.main,
    color: '#fff',
  },
  assistantBubble: {
    backgroundColor: '#555',
    color: '#fff',
  },
}));

export default function ChatMessage({ message }) {
  const classes = useStyles();
  const isUser = message.sender === 'user';

  return (
    <div className={`${classes.messageRow} ${isUser ? classes.userRow : classes.assistantRow}`}>
      <Paper className={`${classes.bubble} ${isUser ? classes.userBubble : classes.assistantBubble}`}>
        <Typography variant="body2">
          {message.text}
        </Typography>
      </Paper>
    </div>
  );
}
