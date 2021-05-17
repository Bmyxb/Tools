echo "Begin" > date_loop.log
echo "Date:"`date` >> date_loop.log

begin_date=20210502
end_date=20210511

while (( $begin_date <= $end_date ))
do
  echo $begin_date >> date_loop.log
  date_param=`date +"%Y-%m-%d %H:%M:%S"`
  hours=`date +%H`
  # do something
  begin_date=`date -d "$begin_date next-day" +%Y%m%d`
done

echo "End" >> date_loop.log