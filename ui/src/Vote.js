import React from 'react';
import { connect } from 'react-redux'
import { withStyles } from 'material-ui/styles';
import Table, { TableBody, TableCell, TableHead, TableRow } from 'material-ui/Table';
import Typography from 'material-ui/Typography'
import Paper from 'material-ui/Paper';
import Button from 'material-ui/Button';
import Dialog, {
  DialogActions,
  DialogContent,
  DialogContentText,
  DialogTitle,
} from 'material-ui/Dialog';
import VoteIcon from '@material-ui/icons/BookmarkBorder'

import {doGetSnacks, getSnacks, doSendVote, sendVote} from './store/actions'

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

class VoteTable extends React.Component {
  constructor(props) {
    super(props)
    this.props.handleGetSnacks()
  }


  render () {
    const { classes } = this.props;

    var content
    var remaining = this.props.remainingVotes == null ?
      null
      : (<Typography>{`Remaining votes: ${this.props.remainingVotes}`}</Typography>)

    if (this.props.fetching) {
      content = (
        <Typography variant="title" noWrap>{'Please wait, fetching snacks...'}</Typography>
      )
    } else {
      content = (
        <div>
          <Paper className={classes.root}>
            <Typography variant="title" noWrap>{'Vote for Suggested Snacks'}</Typography>
            {remaining}
          </Paper>
          <Paper className={classes.root}>
            <Table className={classes.table}>
              <TableHead>
                <TableRow>
                  <TableCell>Name</TableCell>
                  <TableCell numeric>Current Votes</TableCell>
                  <TableCell>Last Purchase Date</TableCell>
                  <TableCell>Vote!</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {this.props.suggestions.map(n => {
                  return (
                    <TableRow key={n.id}>
                      <TableCell>{n.name}</TableCell>
                      <TableCell numeric>{n.votes}</TableCell>
                      <TableCell>{n.lastPurchaseDate}</TableCell>
                      <TableCell>
                        <Button
                          onClick={() => {this.props.handleVote({snack_id: n.id})}}
                          variant="fab"
                          mini
                          color="primary"
                          className={classes.button}>
                          <VoteIcon />
                        </Button>
                      </TableCell>
                    </TableRow>
                  );
                })}
              </TableBody>
            </Table>
          </Paper>
          <Paper className={classes.root}>
            <Typography variant="title" noWrap>These Snacks are Always Purchased</Typography>
            <Table className={classes.table}>
              <TableHead>
                <TableRow>
                  <TableCell>Name</TableCell>
                  <TableCell numeric>Purchase Count</TableCell>
                  <TableCell>Last Purchase Date</TableCell>
                  <TableCell>Purchase Location</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {this.props.permanent.map(n => {
                  return (
                    <TableRow key={n.id}>
                      <TableCell>{n.name}</TableCell>
                      <TableCell numeric>{n.purchaseCount}</TableCell>
                      <TableCell>{n.lastPurchaseDate}</TableCell>
                      <TableCell>{n.purchaseLocations}</TableCell>
                    </TableRow>
                  );
                })}
              </TableBody>
            </Table>
          </Paper>
        </div>
      )
    }

    return (
      <Paper className={classes.root}>
        <Dialog
          open={this.props.openSnacksDialog}
          onClose={this.handleClose}
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
          open={this.props.openVoteDialog}
          onClose={this.handleClose}
          aria-labelledby="alert-dialog-title"
          aria-describedby="alert-dialog-description"
        >
          <DialogTitle id="alert-dialog-title">{"Error Voting for Snack"}</DialogTitle>
          <DialogContent>
            <DialogContentText id="alert-dialog-description">
              {this.props.voteError}
            </DialogContentText>
          </DialogContent>
          <DialogActions>
            <Button onClick={this.props.clearVoteError} color="primary" autoFocus>
              OK
            </Button>
          </DialogActions>
        </Dialog>
        {content}
      </Paper>
    )
  }
}

const mapStateToProps = (state, ownProps) => {
  return {
    suggestions: state.snacks.items.suggestedCurrent,
    permanent: state.snacks.items.permanent,
    fetching: state.snacks.inprocess,
    snacksError: state.snacks.error,
    openSnacksDialog: Boolean(state.snacks.error),
    voteError: state.vote.error,
    openVoteDialog: Boolean(state.vote.error),
    remainingVotes: state.vote.remaining
  }
}

const mapDispatchToProps = (dispatch) => {
  return {
    handleGetSnacks: () => dispatch(doGetSnacks()),
    clearSnacksError: () => dispatch(getSnacks({status: 'clearError'})),
    handleVote: (snack) => dispatch(doSendVote(snack)),
    clearVoteError: () => dispatch(sendVote({status: 'clearError'}))
  }
}

const ConnectedVoteTable = connect(
  mapStateToProps,
  mapDispatchToProps
)(VoteTable)

export default withStyles(styles)(ConnectedVoteTable)
