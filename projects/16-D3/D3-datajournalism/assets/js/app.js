function makeResponsive(){

    // if the SVG area isn't empty when the browser loads,
    // remove it and replace it with a resized version of the chart
    var svgArea = d3.select("body").select("svg");

    //clear svg if it is not empty
    if(!svgArea.empty()){
        svgArea.remove();
    }

    // SVG wrapper dimensions are determined by the current width and
    // height of the browser window.
    var svgWidth = window.innerWidth;
    var svgHeight = window.innerHeight;

    var margin = {
        top: 150,
        bottom: 150,
        right: 150,
        left: 150
    };
    
    var height = svgHeight - margin.top - margin.bottom;
    var width = svgWidth - margin.left - margin.right;

    // append svg element
    var svg = d3
            .select("#scatter")
            .append("svg")
            .attr("height", svgHeight)
            .attr("width", svgWidth);

    // append group element
    var scatterGroup = svg.append("g")
            .attr("transform", `translate(${margin.left}, ${margin.top})`);

    // Initial Params
    var chosenXAxis = "poverty";
    var chosenYAxis = "healthcare";

    //--------------------------------
    // Axis Label Click Functions
    //--------------------------------

    // Updates x scale when click on axis label
    function xScale(data, chosenXAxis){
        var xLinearScale = d3.scaleLinear()
            .domain([d3.min(data, d=> d[chosenXAxis])*0.8, 
                d3.max(data, d=> d[chosenXAxis])*1.2
            ])
            .range([0, width]); 
        return xLinearScale;
    }

    // Updates x Axis when click on axis label
    function renderXAxes(newXScale, xAxis){
        var bottomAxis = d3.axisBottom(newXScale);

        xAxis.transition()
            .duration(300)
            .call(bottomAxis);

        return xAxis;
    }

    // Updates y scale when click on axis label
    function yScale(data, chosenYAxis){
        var yLinearScale = d3.scaleLinear()
            .domain([d3.min(data, d=> d[chosenYAxis])*0.8,
                d3.max(data, d=>d[chosenYAxis])*1.2
            ])
            .range([height, 0])
        return yLinearScale;
    }

    // Updates y Axis when click on axis label
    function renderYAxes(newYScale, yAxis){
        var leftAxis = d3.axisLeft(newYScale);

        yAxis.transition()
            .duration(300)
            .call(leftAxis);
        
        return yAxis;
    }

    // Updates data points group
    function renderCircles(circlesGrp, newXScale, chosenXAxis, newYScale, chosenYAxis){
        circlesGrp.transition()
            .duration(300)
            .attr("cx", d=> newXScale(d[chosenXAxis]))
            .attr("cy", d=> newYScale(d[chosenYAxis]));
        return circlesGrp;
    }

    function renderCircleLabels(circleLabels, newXScale, chosenXAxis, newYScale,  chosenYAxis){
        circleLabels.transition()
            .duration(300)
            .attr("x", d=> newXScale(d[chosenXAxis]))
            .attr("y", d=> newYScale(d[chosenYAxis])+3);
        return circleLabels;
    }

    // Updates tooltips of data points grp 
    function updateToolTip(chosenXAxis, chosenYAxis, circlesGrp){
        // x label for tool tip
        if(chosenXAxis === "poverty"){
            var xlabel = "In Poverty (%):";
        }
        else if(chosenXAxis === "age"){
            var xlabel = "Age (Median):";
        }

        else {
            var xlabel = "Household Income (Median):";
        }

        // y label for tool tip
        if(chosenYAxis === "healthcare"){
            var ylabel = "Lacks Healthcare (%):";
        }
        else if(chosenYAxis === "smokes"){
            var ylabel = "Smokes (%):";
        }

        else {
            var ylabel = "Obesity (%):";
        }

        var toolTip = d3.tip()
            .attr("class", "tooltip")
            .offset([80,-60])
            .html(function(d){
                return(`${d.state}<br>${xlabel} ${d[chosenXAxis]} <br>${ylabel} ${d[chosenYAxis]}`);
            });
        
        circlesGrp.call(toolTip);

        circlesGrp.on("mouseover", function(data){
            toolTip.show(data);
        })
            .on("mouseout", function(data, index){
                toolTip.hide(data);
            });
        return circlesGrp;
    }   

    // import csv
    d3.csv("data.csv").then(function(data, err) {
        if(err) throw err;

        // parse data
        data.forEach(function(data) {
            // X data
            data.poverty = +data.poverty;
            data.age = +data.age;
            data.income = +data.income;
            // Y data
            data.healthcare = +data.healthcare;
            data.smokes = +data.smokes;
            data.obesity = +data.obesity;
        });

        // create scales
        // xLinearScale function 
        var xLinearScale = xScale(data, chosenXAxis);

        // yLinearScale function
        var yLinearScale = yScale(data, chosenYAxis);
    
        // Create initial axis functions
        var bottomAxis = d3.axisBottom(xLinearScale);
        var leftAxis = d3.axisLeft(yLinearScale);

        // Append x axis
        var xAxis = scatterGroup.append("g")
            .classed("x-axis", true)
            .attr("transform", `translate(0,${height})`)
            .call(bottomAxis);

        // Append y axis
        var yAxis = scatterGroup.append("g")
            .classed("y-axis", true)
            //.attr("transform", `translate()`)
            .call(leftAxis);
        
        // Append initial circles
        var circlesGrp = scatterGroup.selectAll("circle")
            .data(data)
            .enter()
            .append("circle")
            .attr("cx", d=> xLinearScale(d[chosenXAxis]))
            .attr("cy", d=> yLinearScale(d[chosenYAxis]))
            .attr("r", 10)
            .attr("fill", "lightblue")
            .attr("opacity", ".8");
        
        var circleLabels = scatterGroup.selectAll(null)
            .data(data)
            .enter()
            .append("text");
        circleLabels
            .attr("x", d=> xLinearScale(d[chosenXAxis]))
            .attr("y", d=> yLinearScale(d[chosenYAxis])+3)
            .text(function(d) {
                return d.abbr;
            })
            .attr("font-size", "10px")
            .attr("text-anchor", "middle")
        //     .selectAll(null)
        //     .append("text")
        //     .attr('dy', '0.35em')
        //     .attr('dx', '0.35em')
        //     .text(d=> d.abbr);

        // Create group for 3 x axis labels
        var xlabelsGroup = scatterGroup.append("g")
            .attr("transform", `translate(${width / 3}, ${height + 20})`);

        var povertyLabel = xlabelsGroup.append("text")
            .attr("x", 0)
            .attr("y", 20)
            .attr("value", "poverty") // value to get for event listener
            .classed("active", true)
            .text("In Poverty (%)");

        var ageLabel = xlabelsGroup.append("text")
            .attr("x", 0)
            .attr("y", 40)
            .attr("value", "age") // value to get for event listener
            .classed("inactive", true)
            .text("Age(Median)");
        
        var incomeLabel = xlabelsGroup.append("text")
            .attr("x", 0)
            .attr("y", 60)
            .attr("value", "income")
            .classed("inactive", true)
            .text("Household Income (Median)");

        // Create group for 3 y axis labels
        var ylabelsGroup = scatterGroup.append("g")
            .attr("transform", "rotate(-90)");

        var healthcareLabel = ylabelsGroup.append("text")
            .attr("y", 0- margin.left+60)
            .attr("x", 0- (height /2))
            .attr("value", "healthcare")
            //.attr("dy", "1em")
            .classed("active", true)
            .text("Lacks Healthcare(%)");
        
        var smokesLabel = ylabelsGroup.append("text")
            .attr("y", 0- margin.left+40)
            .attr("x", 0-(height/2))
            .attr("value", "smokes")
            .classed("inactive", true)
            .text("Smokes (%)");

        var obeseLabel = ylabelsGroup.append("text")
            .attr("y", 0-margin.left+20)
            .attr("x", 0-(height/2))
            .attr("value", "obesity")
            .classed("inactive", true)
            .text("Obesity (%)");
        
        // Update tooltip function 
        var circlesGrp = updateToolTip(chosenXAxis, chosenYAxis, circlesGrp);

        // EVENT LISTENERS for x and y axis

        // x axis event listener
        xlabelsGroup.selectAll("text")
            .on("click", function(){
                //get value of selection
                var value = d3.select(this).attr("value");
                if(value !== chosenXAxis){
                    // replace chosenXAxis with value
                    chosenXAxis = value;
                    console.log(chosenXAxis);

                    // Updates x scale for new selection
                    xLinearScale = xScale(data, chosenXAxis);
                    

                    // Updates x axis for new selection
                    xAxis = renderXAxes(xLinearScale, xAxis);
                    

                    // Updates circles with new selection
                    circlesGrp = renderCircles(circlesGrp, xLinearScale, chosenXAxis, yLinearScale, chosenYAxis);

                    // Updates circle labels with new selection
                    circleLabels = renderCircleLabels(circleLabels, xLinearScale, chosenXAxis, yLinearScale, chosenYAxis);

                    // Updates tooltips with new selection
                    circlesGrp = updateToolTip(chosenXAxis, chosenYAxis, circlesGrp);

                    // Change classes to highlight new selection
                    if(chosenXAxis === "poverty"){
                        povertyLabel
                            .classed("active", true)
                            .classed("inactive", false);
                        ageLabel
                            .classed("active", false)
                            .classed("inactive", true);
                        incomeLabel
                            .classed("active", false)
                            .classed("inactive", true);
                    }
                    else if(chosenXAxis === "age"){
                        povertyLabel
                            .classed("active", false)
                            .classed("inactive", true);
                        ageLabel
                            .classed("active", true)
                            .classed("inactive", false);
                        incomeLabel
                            .classed("active", false)
                            .classed("inactive", true);
                    }
                    else{
                        povertyLabel
                            .classed("active", false)
                            .classed("inactive", true);
                        ageLabel
                            .classed("active", false)
                            .classed("inactive", true);
                        incomeLabel
                            .classed("active", true)
                            .classed("inactive", false);
                    }
                }

            })
        
        ylabelsGroup.selectAll("text")
            .on("click", function(){
                //get value of selection
                var value = d3.select(this).attr("value");
                if(value !== chosenYAxis){
                    // replace chosenYAxis with value
                    chosenYAxis = value;
                    console.log(chosenYAxis);

                    // Updates y scale for new selection
                    yLinearScale = yScale(data, chosenYAxis);

                    // Updates y axis for new selection
                    yAxis = renderYAxes(yLinearScale, yAxis);

                    // Updates circles with new selection
                    circlesGrp = renderCircles(circlesGrp, xLinearScale, chosenXAxis, yLinearScale, chosenYAxis);

                    // Updates circle labels with new selection
                    circleLabels = renderCircleLabels(circleLabels, xLinearScale, chosenXAxis, yLinearScale, chosenYAxis);

                    // Updates tooltips with new selection
                    circlesGrp = updateToolTip(chosenXAxis, chosenYAxis, circlesGrp);

                    // Change classes to highlight new selection
                    if(chosenYAxis === "healthcare"){
                        healthcareLabel
                            .classed("active", true)
                            .classed("inactive", false);
                        smokesLabel
                            .classed("active", false)
                            .classed("inactive", true);
                        obeseLabel
                            .classed("active", false)
                            .classed("inactive", true);
                    }
                    else if (chosenYAxis === "smokes"){
                        healthcareLabel
                            .classed("active", false)
                            .classed("inactive", true);
                        smokesLabel
                            .classed("active", true)
                            .classed("inactive", false);
                        obeseLabel
                            .classed("active", false)
                            .classed("inactive", true);
                    }
                    else {
                        healthcareLabel
                            .classed("active", false)
                            .classed("inactive", true);
                        smokesLabel
                            .classed("active", false)
                            .classed("inactive", true);
                        obeseLabel
                            .classed("active", true)
                            .classed("inactive", false);
                    }
                }
            });
}).catch(function(error){
    console.log(error);
});
}

// makeResponsive() called when browser loads
makeResponsive();

// makeResponsive() called when browser window resized.
d3.select(window).on("resize", makeResponsive);

