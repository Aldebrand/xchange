import { makeStyles, createStyles, Theme } from '@material-ui/core/styles';
import Grid from '@material-ui/core/Grid';
import './App.css';
import Exchange from './Exchange';
import ConfigCommission from './Config'


const useStyles = makeStyles((theme: Theme) =>
  createStyles({
    root: {
      flexGrow: 1,
      margin: "auto",
      marginTop: "200px",
      width: "50%"
    },
    action: {
      marginRight :'50px'
    } 
  }),
);

function App() {
  const classes = useStyles();

  return (
    <Grid container className={classes.root} spacing={2}>
      <Grid item xs={4} className={classes.action}>
        <div>
          <Exchange></Exchange>
        </div>
      </Grid>
      <Grid item xs={4}>
        <ConfigCommission></ConfigCommission>
      </Grid>
    </Grid>
  );
}

export default App;
