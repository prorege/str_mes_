import notify from 'devextreme/ui/notify';

const notifyInfo = (message, opts = {}) => {
  notify({ message: message, width: 450, ...opts }, 'info', 2000);
};

const notifyError = (message, opts = {}) => {
  notify({ message: message, width: 450, ...opts }, 'error', 2000);
};

export { notifyInfo, notifyError };
