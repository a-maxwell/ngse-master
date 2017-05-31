app.controller('studyController', function($rootScope, $scope, $routeParams, $location, formService, authService, userService, messageService) {

    $scope.data = {
        "Master of Science": ["CE", "ChE", "CS", "EE", "EgyE", "EnE", "GmE", "IE", "ME", "MetE", "MSE"],
        "Doctor of Philosophy": ["CE", "ChE", "EEE", "EnE", "EgyE", "MSE"],
        "Master of Engineering": ["EE", "IE"],
        "Doctor of Engineering": ["ChE", "EEE"]
    };

    $scope.fields = {
        "CE": ["Geotechnical", "Structural", "Transportation", "Water Resources"],
        "ChE": ["Biological Engineering", "Environmental Engineering", "Fuel Energy & Thermal Systems", "Materials & Catalyst", "Process Systems Engineering"],
        "CS": ["Algorithms & Complexity", "Computer Security", "Computer Vision & Machine Intelligence", "Network & Distributed Systems", "Scientific Computing", "Software Engineering & Service Sciences", "Web Science"],
        "EE": ["Computers & Communications", "Instrumentation & Control", "Microelectronics", "Power Systems"],
        "EgyE": ["Renewable Energy", "Energy Storage", "Biofuels", "Resource Assessment", "Energy Planning", "Energy Modeling", "Waste-to-Energy", "Others:"],
        "EnE": ["Air Quality Management", "Environmental Management", "Geoenvironmental Engineering", "Solid & Hazardous Waste Management", "Water Quality Management"],
        "GmE": ["Applied Geodesy", "Geoinformatics", "Remote Sensing & Photogrammetry"],
        "IE": ["Production Systems", "Human Factors & Ergonomics", "Operations Research", "Information Systems"],
        "ME": ["Automation, Control & Robotics", "Biomechanics", "Computational Mechanics", "Fluids Engineering", "Heating, Ventilation, Air Conditioning & Refrigeration", "Machine Design", "Power", "Vehicle Engineering"],
        "MetE": ["Minerals Processing", "Metal Extraction", "Physical Metallurgy", "Ultrafine Processing"],
        "MSE": ["Metals and Alloys", "Ceramic Materials", "Polymeric Materials", "Composite Materials", "Semiconductor Materials", "Biomaterials", "Nanomaterials", "Materials for Energy", "Green & Environmental Materials", "High-Value Adding of Local Materials", "Materials Forensics (e.g. Corrosion Engineering and Failure Analysis)"],
    }
    $scope.levels = Object.keys($scope.data);

    var def = {};
    def.level = $scope.levels[0];
    def.program = $scope.data[def.level][0];
    def.program_type = "thesis";
    def.student_type = "full";
    def.choice_1 = "";
    def.choice_2 = "";
    def.choice_3 = "";
    def.adviser = "";
    def.start_of_study = "first";
    def.year = "";
    def.other_scholarship = "no";
    def.other_scholarship_name = "";

    function sleep(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }

    function initWatch() {
        $scope.$watch('user["program"]', function(newValue, oldValue, scope) {
            if (newValue != oldValue) {
                $scope.user.choice_1 = "";
                $scope.user.choice_2 = "";
                $scope.user.choice_3 = "";
            }
        });
    }

    async function initController() {
        $scope.loading = true;
        userService.fetchUser(function(data) {
            $scope.user = data;
            filterUser();
            initWatch();
            $scope.loading = false;
        });
    };


    $scope.years = ["2017-2018", "2018-2019", "2019-2020", "2020-2021"];

    $scope.programs = $scope.data["Master of Science"];

    $scope.user = def;
    initController();

    $scope.availableProgram = availableProgram;
    $scope.nonThesisOption = nonThesisOption;
    $scope.thesisOption = thesisOption;
    $scope.otherScholarship = otherScholarship;
    $scope.filter_c2 = filter_c2;
    $scope.filter_c3 = filter_c3;
    $scope.check_c2 = check_c2;
    $scope.check_c3 = check_c3;
    $scope.debug = debug;
    $scope.submit = submit;

    $scope.resetLabs = resetLabs;

    $scope.always = true; // what is this for

    function check() {
        return false;
    }

    function debug() {
        console.log($scope.user);
        console.log(userService.answered());
    }

    function resetLabs() {
        user.choice_1 = "";
        user.choice_2 = "";
        user.choice_3 = "";
    }

    function check_c3() {
        if ($scope.user.choice_2 === "") return "disabled";
    }

    function check_c2() {
        console.log($scope.user.choice_1);
        if ($scope.user.choice_1 === "") return "disabled";
        return "";
    }

    function filter_c3() {
        if ($scope.user.choice_2 === "") return [];
        var labs = [];
        for (var i = 0; i < $scope.fields[$scope.user.program].length; i++) {
            if ($scope.fields[$scope.user.program][i] != $scope.user.choice_1 && $scope.fields[$scope.user.program][i] != $scope.user.choice_2) {
                labs.push($scope.fields[$scope.user.program][i]);
            } 
        }
        return labs;
    }

    function filter_c2() {
        if ($scope.user.choice_1 === "") return [];
        var labs = [];
        for (var i = 0; i < $scope.fields[$scope.user.program].length; i++) {
            if ($scope.fields[$scope.user.program][i] != $scope.user.choice_1) {
                labs.push($scope.fields[$scope.user.program][i]);
            } 
        }
        return labs;
    }

    function otherScholarship() {
        return ($scope.user.other_scholarship === "yes");
    }

    function thesisOption() {
        return ($scope.user.program_type === "thesis");
    }

    function nonThesisOption() {
        var programs = ["CE", "ChE", "MSE"]
        if ($scope.user.level != "Master of Science") {
            $scope.user.program_type = "thesis";
            return false;
        }
        for (var i = 0; i < programs.length; i++) if ($scope.user.program === programs[i]) return true;
        $scope.user.program_type = "thesis";
        return false;
    }

    function availableProgram(p) {
        if ($scope.data[$scope.user.level] === undefined) return false;
        var change = true;
        for (var i = 0; i < $scope.data[$scope.user.level].length; i++) if ($scope.data[$scope.user.level][i] === p) return true;
        for (var i = 0; i < $scope.data[$scope.user.level].length; i++) if ($scope.data[$scope.user.level][i] === $scope.user.program) change = false;
        if (change) $scope.user.program = $scope.data[$scope.user.level][0];
        return false;
    }

    function filterUser() {

        var keys = Object.keys(def);

        for (var i = 0; i < keys.length; i++) {
            if ($scope.user[keys[i]] === null) $scope.user[keys[i]] = def[keys[i]];
            if ($scope.user[keys[i]] === "") $scope.user[keys[i]] = def[keys[i]];
        }
    }

    function checkAnswers() {
        /* check the following:
        1. choices
        2. program
        3. program type
        4. student type
        5. start of study
        6. other scholarship */
        var u = $scope.user;

        console.log('woop');
        if (thesisOption() && (u.choice_1 === "" || u.choice_2 === "" || u.choice_2 === "")) {
            messageService.pushMessage({
                text: 'Please complete research field choices.',
                type: 'error'
            });
            return false; // thesis option but no choices
        }

        console.log('dee');
        if (u.year === "") {
            messageService.pushMessage({
                text: 'Please type in academic year.',
                type: 'error'
            });
            return false; // no year input
        }

        console.log('doo');
        if (u.other_scholarship === "yes" && u.other_scholarship_name === "") {
            messageService.pushMessage({
                text: 'Please type in the name of your scholarship.',
                type: 'error'
            });
            return false; // other scholarship name is blank but has other scholarship
        }

        return true;
    }

    function submit() {
        $scope.loading = true;
        if (checkAnswers()) {
            userService.saveAnswers(function(data) {
                $scope.loading = false;
                $scope.user = userService.getUser();
                console.log(data);
                if (data.success) {
                    messageService.pushMessage({
                        text: 'Program of Study saved',
                        type: 'info'
                    });
                    $location.path('/application');
                } else {
                    messageService.pushMessage({
                        text: 'Something happened. Please try submitting again.',
                        type: 'warning'
                    });
                }
            }, $scope.user);
        } else {
            $scope.loading = false;
        }
    }

});