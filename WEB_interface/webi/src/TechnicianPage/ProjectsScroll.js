
import './ProjectScroll.scss'
import { FixedSizeList } from 'react-window';
import Box from '@mui/material/Box';
import ListItem from '@mui/material/ListItem';
import ListItemButton from '@mui/material/ListItemButton';
import ListItemText from '@mui/material/ListItemText';
import ListSubheader from '@mui/material/ListSubheader';
import List from '@mui/material/List';
export default function ProjectScroll({ name, listTasks }) {

    const renderContent = () => {
        return (
            <li key={`section-${name}`}>
                <ul>
                    <ListSubheader>{name}</ListSubheader>
                    {listTasks.map(([taskName, taskLength]) => (


                        <ListItem key={`item-${taskName}-${taskLength}`}>
                            <ListItemText primary={`${taskName} (duração: ${taskLength})`} />
                        </ListItem>


                    ))}
                </ul>
            </li>
        )

    }

    return (
        <div className="projectLine ">
            <List
                sx={{
                    width: '100%',
                    maxWidth: 360,
                    bgcolor: 'background.paper',
                    position: 'relative',
                    overflow: 'auto',
                    maxHeight: 300,
                    '& ul': { padding: 0 },
                }}
                subheader={<li />}
            >
                {renderContent()}
            </List>
        </div>
    )
    // {listTasks.map((task, index) => renderProjectBox(task, index))}
}