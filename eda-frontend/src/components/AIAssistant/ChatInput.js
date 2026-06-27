import React, { useState, useEffect } from 'react';
import { TextField, IconButton, makeStyles } from '@material-ui/core';
import SendIcon from '@material-ui/icons/Send';

const useStyles = makeStyles((theme) => ({
  inputContainer: {
    display: 'flex',
    alignItems: 'center',
    padding: theme.spacing(1),
    backgroundColor: '#2d2d2d',
    borderTop: '1px solid #555',
  },
  textField: {
    flex: 1,
    backgroundColor: '#404040',
    borderRadius: 4,
    '& .MuiInputBase-root': {
      color: '#fff',
    },
    '& .MuiOutlinedInput-notchedOutline': {
      border: 'none',
    },
  },
  sendButton: {
    color: theme.palette.primary.main,
    '&.Mui-disabled': {
      color: '#666',
    },
  },
}));

export default function ChatInput({ onSend, disabled, inputRef, prefillMessage, onPrefillClear }) {
  const classes = useStyles();
  const [text, setText] = useState('');

  useEffect(() => {
    if (prefillMessage) {
      setText(prefillMessage);
      if (onPrefillClear) onPrefillClear();
    }
  }, [prefillMessage, onPrefillClear]);

  const handleSend = () => {
    const trimmed = text.trim();
    if (trimmed && !disabled) {
      onSend(trimmed);
      setText('');
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className={classes.inputContainer}>
      <TextField
        inputRef={inputRef}
        className={classes.textField}
        multiline
        rowsMax={4}
        variant="outlined"
        placeholder="Ask the AI assistant..."
        value={text}
        onChange={(e) => setText(e.target.value)}
        onKeyDown={handleKeyDown}
        disabled={disabled}
        size="small"
      />
      <IconButton 
        className={classes.sendButton}
        onClick={handleSend} 
        disabled={disabled || !text.trim()}
        aria-label="send message"
      >
        <SendIcon />
      </IconButton>
    </div>
  );
}
