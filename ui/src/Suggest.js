import React from 'react'
import { connect } from 'react-redux'
import { withStyles } from 'material-ui/styles';
import Table, { TableBody, TableCell, TableHead, TableRow } from 'material-ui/Table';
import Typography from 'material-ui/Typography'
import TextField from 'material-ui/TextField';
import Paper from 'material-ui/Paper';
import Button from 'material-ui/Button';
import Dialog, {
  DialogActions,
  DialogContent,
  DialogContentText,
  DialogTitle,
} from 'material-ui/Dialog';
import EditIcon from '@material-ui/icons/BorderColor'
import {doGetSnacks, getSnacks, sendSnack, doSendSnack} from './store/actions'


const styles = theme => ({
  root: {
    width: '100%',
    marginTop: theme.spacing.unit * 3,
    overflowX: 'auto',
  },
  table: {
    minWidth: 700,
  },
});


class Suggest extends React.Component {
  constructor(props) {
    super(props)
    this.props.handleGetSnacks()

    this.state = {
      snack: {
        name: '',
        location: ''
      }
    }

    this.handleSnackNameChange = this.handleSnackNameChange.bind(this)
    this.handleSnackLocationChange = this.handleSnackLocationChange.bind(this)
    this.suggestFormWrapper = this.suggestFormWrapper.bind(this)
  }

  handleSnackNameChange(event) {
    this.setState({snack: { name: event.target.value, location: this.state.snack.location}})
  }

  handleSnackLocationChange(event) {
    this.setState({snack: { location: event.target.value, name: this.state.snack.name}})
  }

  suggestFormWrapper() {
    this.props.handleSuggest(this.state.snack)
    this.setState({snack: {name: '', location: ''}})
  }

  render () {
    const { classes } = this.props;

    var errorDialog = (
      <Paper className={classes.root}>
        <Dialog
          open={this.props.openSnacksDialog}
          onClose={this.props.clearSnacksError}
          aria-labelledby="alert-dialog-title"
          aria-describedby="alert-dialog-description"
        >
          <DialogTitle id="alert-dialog-title">{"Error Fetching Snacks"}</DialogTitle>
          <DialogContent>
            <DialogContentText id="alert-dialog-description">
              {this.props.snacksError}
            </DialogContentText>
          </DialogContent>
          <DialogActions>
            <Button onClick={this.props.clearSnacksError} color="primary" autoFocus>
              OK
            </Button>
          </DialogActions>
        </Dialog>
        <Dialog
          open={this.props.openSuggestDialog}
          onClose={this.props.clearSuggestError}
          aria-labelledby="alert-dialog-title"
          aria-describedby="alert-dialog-description"
        >
          <DialogTitle id="alert-dialog-title">{"Error Suggesting Snacks"}</DialogTitle>
          <DialogContent>
            <DialogContentText id="alert-dialog-description">
              {this.props.suggestError}
            </DialogContentText>
          </DialogContent>
          <DialogActions>
            <Button onClick={this.props.clearSuggestError} color="primary" autoFocus>
              OK
            </Button>
          </DialogActions>
        </Dialog>
      </Paper>
    )

    var suggestionForm = (
      <div>
        <DialogTitle id="form-dialog-title">Suggest a new Snack</DialogTitle>
        <DialogContent>
          <TextField
            autoFocus
            margin="dense"
            id="snackName"
            label="Snack Name"
            type="text"
            value={this.state.snack.name}
            onChange={this.handleSnackNameChange}
            fullWidth
          />
          <TextField
            margin="dense"
            id="snackLocation"
            label="Snack Purchase Location"
            type="text"
            value={this.state.snack.location}
            onChange={this.handleSnackLocationChange}
            fullWidth
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={this.suggestFormWrapper} color="primary">
            Submit
          </Button>
        </DialogActions>
      </div>
    )

    var content
    if (this.props.fetching) {
      content = (
        <Typography variant="title" noWrap>{'Please wait, fetching snacks...'}</Typography>
      )
    } else {
      content = (
        <Paper className={classes.root}>
          <Paper className={classes.root}>
            <Typography variant="title" noWrap>{'Suggest a previously suggested snack'}</Typography>
          </Paper>
          <Paper className={classes.root}>
            <Table className={classes.table}>
              <TableHead>
                <TableRow>
                  <TableCell>Name</TableCell>
                  <TableCell>Purchase Location</TableCell>
                  <TableCell>Suggest Again!</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {this.props.suggestions.map(n => {
                  return (
                    <TableRow key={n.id}>
                      <TableCell>{n.name}</TableCell>
                      <TableCell>{n.purchaseLocations}</TableCell>
                      <TableCell>
                        <Button
                          onClick={() => {this.props.handleSuggest({name: n.name, location: n.purchaseLocations})}}
                          variant="fab"
                          mini
                          color="primary"
                          className={classes.button}>
                          <EditIcon />
                        </Button>
                      </TableCell>
                    </TableRow>
                  );
                })}
              </TableBody>
            </Table>
          </Paper>
        </Paper>
      )
    }
    return (
      <div>
        {errorDialog}
        {suggestionForm}
        {content}
      </div>
    )
  }
}


const mapStateToProps = (state, ownProps) => {
  return {
    suggestions: state.snacks.items.suggestedExpired,
    fetching: state.snacks.inprocess,
    snacksError: state.snacks.error,
    openSnacksDialog: Boolean(state.snacks.error),
    suggestError: state.snacks.post.error,
    openSuggestDialog: Boolean(state.snacks.post.error),
  }
}

const mapDispatchToProps = (dispatch) => {
  return {
    handleGetSnacks: () => dispatch(doGetSnacks()),
    clearSnacksError: () => dispatch(getSnacks({status: 'clearError'})),
    handleSuggest: (snack) => dispatch(doSendSnack(snack)),
    clearSuggestError: () => dispatch(sendSnack({status: 'clearError'}))
  }
}

const ConnectedSuggest = connect(
  mapStateToProps,
  mapDispatchToProps
)(Suggest)


export default withStyles(styles)(ConnectedSuggest)
