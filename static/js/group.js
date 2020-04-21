

const planning_unit = document.getElementById("id_planning_unit");
const deadline_week = document.getElementById("deadline_week");
const deadline_day = document.getElementById("deadline_day");

planning_unit.addEventListener(
    'change', () => {
        if (planning_unit.value == "week") {
            deadline_week.hidden = false;
            deadline_day.hidden = true;

        }
        else {
            deadline_week.hidden = true;
            deadline_day.hidden = false;
        }
    }
)