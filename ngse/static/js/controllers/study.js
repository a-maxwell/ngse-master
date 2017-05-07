app.controller('studyController', function($rootScope, $scope, $routeParams, $location, formService, authService, userService) {

    $scope.data = {
        "Master of Science": ["CE", "ChE", "CS", "EE", "EgyE", "EnE", "GmE", "IE", "ME", "MetE", "MSE"],
        "Doctor of Philosophy": ["CE", "ChE", "EEE", "EnE", "EgyE", "MSE"],
        "Master of Engineering": ["EE", "IE"],
        "Doctor of Engineering": ["ChE", "EEE", "EgyE"]
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

    function initWatch() {
        $scope.$watch('user["program"]', function(newValue, oldValue, scope) {
            if (newValue != oldValue) {
                $scope.user.choice_1 = "";
                $scope.user.choice_2 = "";
                $scope.user.choice_3 = "";
            }
        });
    }

    function initController() {
        if (userService.getUser() === {}) {
            userService.fetchUser(function(data) {
                console.log(data);
                $scope.user = data;
                filterUser();
                console.log($scope.user);
                initWatch();
            });
        } else {
            $scope.user = userService.getUser();
            filterUser();
            console.log($scope.user);
            initWatch();
        }
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

    $scope.always = true;

    function submit() {
        $scope.debug();
        userService.saveAnswers(function(data) {
            $scope.user = userService.getUser();
            console.log(data);
            if (data.success) $location.path('/application');
        }, $scope.user);
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
        }
    }

});