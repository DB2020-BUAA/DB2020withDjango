$(function () {
    "use strict";

    // small state
    $('.chart_1').sparkline('html', {
        type: 'bar',
        height: '60px',
        barSpacing: 3,
        barWidth: 2,
        barColor: '#17a2b8',
    });
    $('.chart_3').sparkline('html', {
        type: 'bar',
        height: '60px',
        barSpacing: 3,
        barWidth: 2,
        barColor: '#28a745',
    });
    $('.chart_4').sparkline('html', {
        type: 'bar',
        height: '60px',
        barSpacing: 3,
        barWidth: 2,
        barColor: '#45aaf2',
    });
    $('.chart_2').sparkline('html', {
        type: 'bar',
        height: '60px',
        barSpacing: 3,
        barWidth: 2,
        barColor: '#f3ad06',
    });
    // Summary 
    $('.chart').sparkline('html', {
        type: 'bar',
        height: '53px',
        barSpacing: 3,
        barWidth: 2,
        barColor: '#434750',
    });

    $('.knob').knob({
        draw: function () {
        }
    });
});

$(function () {
    "use strict";
    var dataStackedBar = {
        labels: ['Q1', 'Q2', 'Q3', 'Q4', 'Q5', 'Q6'],
        series: [
            [8000, 12000, 3600, 1300, 12000, 12000],
            [2000, 4000, 5000, 3000, 7000, 4000],
            [1000, 2000, 4000, 6000, 3000, 2000]
        ]
    };
    new Chartist.Bar('#stackedbar-chart', dataStackedBar, {
        height: "228px",
        stackBars: true,
        axisX: {
            showGrid: false
        },
        axisY: {
            labelInterpolationFnc: function (value) {
                return (value / 1000) + 'k';
            }
        },
        plugins: [
            Chartist.plugins.tooltip({
                appendToBody: true
            }),
            Chartist.plugins.legend({
                legendNames: ['Blue', 'Pink', 'Orange']
            })
        ]
    }).on('draw', function (data) {
        if (data.type === 'bar') {
            data.element.attr({
                style: 'stroke-width: 25px'
            });
        }
    });
});