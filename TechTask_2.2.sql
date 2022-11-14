select count(title) as amount, ceiling("width"/5)*5 as ceiling_width, ceiling("depth"/5)*5 as ceiling_depth, ceiling("height"/5)*5 as ceiling_heigth  
from notebooks_notebook
group by (ceiling_width, ceiling_depth, ceiling_heigth)
order by ceiling_width desc , ceiling_depth desc , ceiling_heigth desc;