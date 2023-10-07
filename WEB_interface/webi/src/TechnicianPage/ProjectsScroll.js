
import './ProjectScroll.scss'
import { FixedSizeList } from 'react-window';
import Box from '@mui/material/Box';
import ListItem from '@mui/material/ListItem';
import ListItemButton from '@mui/material/ListItemButton';
import ListItemText from '@mui/material/ListItemText';
export default function ProjectScroll({name, listTasks }) {

    console.log(listTasks)

    const renderProjectBox = ([taskName, taskLength], index) => {
        console.log(index)
        return (
                <ListItem  key={index} component="div" disablePadding>
      <ListItemButton>
        <ListItemText primary={taskName} />
      </ListItemButton>
    </ListItem>
        )
    }

    function renderRow(props) {
  const { index, style } = props;
/*return (
    <ListItem style={style} key={index} component="div" disablePadding>
      <ListItemButton>
        {console.log("AQUI")}
        <ListItemText primary={`Item ${index + 1}`} />
      </ListItemButton>
    </ListItem>
  );*/
    return listTasks.map((task, index) => renderProjectBox(task, index))
  
}

    return (
        <div className="projectLine ">
               <Box
      sx={{ width: '100%', height: 400, maxWidth: 360, bgcolor: 'background.paper' }}
    >
<FixedSizeList
        height={400}
        width={360}
        itemSize={listTasks.length}
        itemCount={listTasks.length}
                overscanCount={listTasks.length}
      >
              {renderRow}
      </FixedSizeList>
</Box>
       </div>
    )
    // {listTasks.map((task, index) => renderProjectBox(task, index))}
}