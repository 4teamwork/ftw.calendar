
jq(document).ready(function() {
	jq('#calendar').fullCalendar({
		header: {
			left: 'prev,next today',
			center: 'title',
			right: 'month,agendaWeek,agendaDay'
		},
		monthNames: customMonthNames,
		monthNamesShort: customMonthNamesShort,
		dayNames: customDayNames,
		dayNamesShort: customDayNamesShort,
		buttonText: customButtonText,
		titleFormat: customTitleFormat,
		editable: true,
		startParam: "start:int",
		endParam: "end:int",
		events: "ftwcalendarupdate_view",
        axisFormat: 'H(:mm)',
        allDaySlot: true,
        allDayText: customAllDayText,
        firstDay: 1,
        weekMode: "liquid",
        timeFormat: 'H(:mm)',
        eventRender: function(event, element) {
            element.find("a").attr('title', event.description);
            return element
        },
        eventDrop: function(event, dayDelta, minuteDelta) {
            data = 'event='+event.id+'&dayDelta='+dayDelta+'&minuteDelta='+minuteDelta;
            jq.ajax({
                type :      'POST',
                url :       './calendar_drop',
                data :      data,
                success :   function(msg) {      
                }
            });
            

        },
        eventResize: function(event,dayDelta,minuteDelta,revertFunc) {
            data = 'event=' + event.id + '&dayDelta=' + dayDelta + '&minuteDelta='+ minuteDelta;
            jq.ajax({
                type :      'POST',
                url :       './calendar_resize',
                data :      data,
                success :   function(msg) {
                },
                error : revertFunc
            });
        },
        loading: function(bool) {
            if (bool) {
                jq('#kss-spinner').show();
            } else {
                jq('#kss-spinner').hide();
            }
        }

	});

});
