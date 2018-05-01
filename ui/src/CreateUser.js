import React from 'react';
import PropTypes from 'prop-types'
import { connect } from 'react-redux'
import {Link} from 'react-router-dom'
import {
  createUser,
  doCreateUser
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
    this.handleClose = this.handleClose.bind(this)
  }

  handleUserChange(event) {
    this.setState({user: { username: event.target.value, password: this.state.user.password}})
  }

  handlePasswordChange(event) {
    this.setState({user: { password: event.target.value, username: this.state.user.username}})
  }

  handleClose() {
    this.setState({ errordialog: false })
  }

  handleSubmit () {
    this.props.handleCreateUser(this.state.user)
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
            <DialogTitle id="alert-dialog-title">{"Error Creating User"}</DialogTitle>
            <DialogContent>
              <DialogContentText id="alert-dialog-description">
                {this.props.error}
              </DialogContentText>
            </DialogContent>
            <DialogActions>
              <Button onClick={this.props.clearError} color="primary" autoFocus>
                OK
              </Button>
            </DialogActions>
          </Dialog>
          <DialogTitle id="form-dialog-title">Sign Up</DialogTitle>
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
          </DialogContent>
          <DialogActions>
            <Button component={Link} to="/Login" color="primary">
              Cancel
            </Button>
            <Button onClick={this.handleSubmit} color="primary">
              Create User
            </Button>
          </DialogActions>
        </Paper>
      </div>
    )
  }
}

LoginDialog.propTypes = {
  handleCreateUser: PropTypes.func.isRequired,
}

const mapDispatchToProps = (dispatch) => {
  return {
    handleCreateUser: user => {
      dispatch(doCreateUser(user))
    },
    clearError: () => dispatch(createUser({status: 'clearError'}))
  }
}

const mapStateToProps = (state, ownProps) => {
  return {
    error: state.user.createUser.error,
    openDialog: Boolean(state.user.createUser.error)
  }
}
const ConnectedCreateUser = connect(
  mapStateToProps,
  mapDispatchToProps
)(LoginDialog)

export default ConnectedCreateUser
