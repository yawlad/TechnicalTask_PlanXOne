select notebooks_brand.title as brand, amounts.amount 
from
	notebooks_brand, (select brand_id, count(brand_id) as amount 
	from notebooks_notebook
	group by brand_id
	order by amount desc) as amounts
where notebooks_brand.id = amounts.brand_id
order by amount desc;

