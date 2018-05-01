import React from 'react';
import {Link} from 'react-router-dom'
import PropTypes from 'prop-types'
import { connect } from 'react-redux'
import {
  doLoginUser,
  userLogin
} from './store/actions'
import Button from 'material-ui/Button';
import TextField from 'material-ui/TextField';
import Paper from 'material-ui/Paper';
import Dialog, {
  DialogActions,
  DialogContent,
  DialogContentText,
  DialogTitle,
} from 'material-ui/Dialog';

class LoginDialog extends React.Component {
  constructor(props) {
    super(props)
    this.state = {
      user: {
        username: '',
        password: ''
      }
    }
    this.handleUserChange = this.handleUserChange.bind(this)
    this.handlePasswordChange = this.handlePasswordChange.bind(this)
    this.handleSubmit = this.handleSubmit.bind(this)
  }

  handleUserChange(event) {
    this.setState({user: { username: event.target.value, password: this.state.user.password}})
  }

  handlePasswordChange(event) {
    this.setState({user: { password: event.target.value, username: this.state.user.username}})
  }

  handleSubmit () {
    this.props.handleLoginUser(this.state.user)
  }

  render() {

    return (
      <div>
        <Paper>
          <Dialog
            open={this.props.openDialog}
            onClose={this.handleClose}
            aria-labelledby="alert-dialog-title"
            aria-describedby="alert-dialog-description"
          >
            <DialogTitle id="alert-dialog-title">{"Error Logging In"}</DialogTitle>
            <DialogContent>
              <DialogContentText id="alert-dialog-description">
                {this.props.error}
              </DialogContentText>
            </DialogContent>
            <DialogActions>
              <Button onClick={this.props.handleClose} color="primary" autoFocus>
                OK
              </Button>
            </DialogActions>
          </Dialog>
          <DialogTitle id="form-dialog-title">Log In</DialogTitle>
          <DialogContent>
            <TextField
              autoFocus
              margin="dense"
              id="username"
              label="Username"
              type="text"
              value={this.state.user.username}
              onChange={this.handleUserChange}
              fullWidth
            />
            <TextField
              margin="dense"
              id="password"
              label="Password"
              type="password"
              value={this.state.user.password}
              onChange={this.handlePasswordChange}
              fullWidth
            />
          <DialogContentText>New user? <Link to="/newuser">Create a user</Link></DialogContentText>
          </DialogContent>
          <DialogActions>
            <Button onClick={this.handleClose} color="primary">
              Cancel
            </Button>
            <Button onClick={this.handleSubmit} color="primary">
              Log In
            </Button>
          </DialogActions>
        </Paper>
      </div>
    )
  }
}

LoginDialog.propTypes = {
  handleLoginUser: PropTypes.func.isRequired
}

const mapDispatchToProps = (dispatch) => {
  return {
    handleLoginUser: user => {dispatch(doLoginUser(user))},
    handleClose: () => {dispatch(userLogin({'status': 'clearError'}))}
  }
}

const mapStateToProps = (state) => {
  return {
    error: state.user.login.error,
    openDialog: Boolean(state.user.login.error)
  }
}
const ConnectedLoginDialog = connect(
  mapStateToProps,
  mapDispatchToProps
)(LoginDialog)

export default ConnectedLoginDialog
