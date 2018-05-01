import React from 'react';
import {Route, Switch, Link} from 'react-router-dom'
import PropTypes from 'prop-types';
import { withStyles } from 'material-ui/styles';
import Drawer from 'material-ui/Drawer';
import Button from 'material-ui/Button';
import AppBar from 'material-ui/AppBar';
import Toolbar from 'material-ui/Toolbar';
import Typography from 'material-ui/Typography';
import List, { ListItem, ListItemIcon, ListItemText } from 'material-ui/List';
import EditIcon from '@material-ui/icons/BorderColor'
import VoteIcon from '@material-ui/icons/BookmarkBorder'
import Login from './Login'
import CreateUser from './CreateUser'
import Vote from './Vote'
import Suggest from './Suggest'


const drawerWidth = 240;

const styles = theme => ({
  root: {
    flexGrow: 1,
    zIndex: 1,
    overflow: 'hidden',
    position: 'relative',
    display: 'flex',
  },
  appBar: {
    zIndex: theme.zIndex.drawer + 1,
  },
  drawerPaper: {
    position: 'relative',
    width: drawerWidth,
  },
  content: {
    flexGrow: 1,
    backgroundColor: theme.palette.background.default,
    padding: theme.spacing.unit * 3,
    minWidth: 0, // So the Typography noWrap works
  },
  toolbar: theme.mixins.toolbar,
});

class ClippedDrawer extends React.Component {
  voteView = (
    <Vote />
  )
  suggestView = (
    <Typography noWrap>{'suggest something bish'}</Typography>
  )

  constructor(props) {
    super(props)
    this.state = {
      nav: this.voteView,
      loggedIn: Boolean(sessionStorage.getItem('token'))
    }
    this.handleLoginClick = this.handleLoginClick.bind(this)
  }

  handleVoteView() {
    this.setState({
      nav: this.voteView
    })
  }

  handleSuggestView() {
    this.setState({
      nav: this.suggestView
    })
  }

  handleLoginClick = function () {
    // remove token from session storage
    if (this.state.loggedIn) {
      sessionStorage.clear()
    }
  }

  render() {
    const { classes } = this.props;

    return (
      <div className={classes.root}>
        <AppBar position="absolute" className={classes.appBar}>
          <Toolbar style={{'justifyContent': 'space-between'}}>
            <Typography variant="title" color="inherit" noWrap>
              Nerdery Snacks
            </Typography>
            <Button color="inherit" component={Link} to="/login" onClick={this.handleLoginClick}>{this.state.loggedIn ? 'Log Out' : 'Log In'}</Button>
          </Toolbar>
        </AppBar>
        <Drawer
          variant="permanent"
          classes={{
            paper: classes.drawerPaper,
          }}
        >
          <div className={classes.toolbar} />
          <List>
            <ListItem component={Link} to="/vote" button>
              <ListItemIcon><VoteIcon/></ListItemIcon>
              <ListItemText>Vote for snacks</ListItemText>
            </ListItem>
            <ListItem component={Link} to="/suggest" button>
              <ListItemIcon><EditIcon/></ListItemIcon>
              <ListItemText>Suggest a snack</ListItemText>
            </ListItem>
         </List>
        </Drawer>
        <main className={classes.content}>
          <div className={classes.toolbar} />
          <Switch>
            <Route path="/vote" component={Vote} />
            <Route path="/suggest" component={Suggest} />
            <Route path="/login" component={Login} />
            <Route path="/newuser" component={CreateUser} />
          </Switch>
        </main>
      </div>
    );
  }
}

ClippedDrawer.propTypes = {
  classes: PropTypes.object.isRequired,
};

export default withStyles(styles)(ClippedDrawer);
