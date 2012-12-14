var scoring_board = {
	alert_timer: null,
	id_alert_ctn: 'scoring-board-alert-ctn',
	id_alert: 'scoring-board-alert',
	init: function(opts){
		// Update conf with opts
		$.extend(scoring_board, opts);
	},
	inc_item: function(item_id, value){
		if(value == undefined){ value=1; }
		var item = $(item_id);
		item.html(parseInt(item.html())+value);
	},
	dec_item: function(item_id, value){
		if(value == undefined){ value=1; }
		var item = $(item_id);
		item.html(parseInt(item.html())-value);
	},
	raz_item: function(item_id){
		var item = $(item_id)
		var old_value = parseInt(item.html());
		item.html(0);
		return old_value;
	},
	plus: function(match_id, team_id){
		// Get score
		var score_id = '#'+match_id+'-'+team_id;
		var score = parseInt($(score_id).html());
		if( score < 8){
			// Get ID other team
			var other_team_id = '';
			if(team_id == 'team-1'){ other_team_id = 'team-2'}
			else{ other_team_id = 'team-1'; }
			// Get other team IDs
			var other_score_id = '#'+match_id+'-'+other_team_id;
			var other_total_id = other_score_id+'-total';
			var total_id = score_id+'-total';
			// Add 1 and update total
			scoring_board.inc_item(score_id);
			scoring_board.inc_item(total_id);
			// RAZ score other team
			var to_dec = scoring_board.raz_item(other_score_id);
			// Update other total team
			scoring_board.dec_item(other_total_id, to_dec);
		}
	},
	minus: function(match_id, team_id){
		// Get score
		var score_id = '#'+match_id+'-'+team_id;
		var score = parseInt($(score_id).html());
		if(score > 0){
			// Minus 1 if score > 0
			scoring_board.dec_item(score_id);
			// Update total
			scoring_board.dec_item(score_id+'-total');
		}
	},
	scoring_end: function(match_pk){
		console.log('Socring end : match_pk=', match_pk);
		// Team 1 : score
		var team_1_score_id = '#match-'+match_pk+'-team-1';
		var team_1_score_item = $(team_1_score_id);
		var team_1_score = parseInt(team_1_score_item.html());
		var team_1_item = team_1_score_item.parent('td.result');
		console.log('Team 1: ', team_1_score);
		// Team 2 : score
		var team_2_score_id = '#match-'+match_pk+'-team-2';
		var team_2_score_item = $(team_2_score_id);
		var team_2_score = parseInt(team_2_score_item.html());
		var team_2_item = team_2_score_item.parent('td.result');
		console.log('Team 2: ', team_2_score);
		// PK of winner
		team_winner_item = null;
		score_winner = null;
		if(team_1_score >= team_2_score){
			team_winner_item = team_1_item;
			score_winner = team_1_score;
		}else{
			team_winner_item = team_2_item;
			score_winner = team_2_score;
		}
		var team_pk = team_winner_item.attr('team_pk');
		var end_pk = team_winner_item.attr('end_pk');
		console.log('Team PK: ',team_pk );
		console.log('Match PK: ', match_pk);
		console.log('END PK: ', end_pk);
		console.log('Score winner:', score_winner);
		// POST request
		$.post(scoring_board.url_scoring,
			   {'match_pk': match_pk,
				'team_pk': team_pk,
				'end_pk': end_pk,
				'score': score_winner},
			   function(json){
				   if(json.code_response == 200){
					   // Show msg
					   scoring_board.show_alert(json.msg, 'success');
					   // Save old html controls
					   var team_1_html = team_1_item.html();
					   var team_2_html = team_2_item.html();
					   // Update scores
					   team_1_item.html(team_1_score);
					   team_2_item.html(team_2_score);
					   // If match not finished
					   if(!json.match_finished){
						   // Update display controls
						   team_1_item.next().html(team_1_html);
						   team_2_item.next().html(team_2_html);
						   // RAZ old counter
						   scoring_board.raz_item(team_1_score_id);
						   scoring_board.raz_item(team_2_score_id);
					   }else{
						   // Disable button 'Score' and 'Finish' for match
						   $('#controls-match-'+match_pk).html('');
					   }
					   if(json.all_matches_finished){
						   // Activate "Finish Round" button
						   scoring_board.activate_group_controls();
					   }
				   }else if(json.code_response == 500){
					   console.log('Error:', json.msg);
					   scoring_board.show_alert(json.msg, 'danger');
				   }else{
					   scoring_board.show_alert(('Error unexpected!'), 'danger');
				   }
			   });
	},
	finish_match: function(match_pk){
		// POST request
		$.post(scoring_board.url_finish_match,
			   {'match_pk': match_pk},
			   function(json){
				   var msg_type = 'success';
				   if(json.code_response == 200){
					   if(json.match_finished){
						   // Disable controls for match.
						   $('#controls-match-'+match_pk).html('');
						   // Empty results
						   $('#match-'+match_pk+'-team-1').parent('td.result').html('');
						   $('#match-'+match_pk+'-team-2').parent('td.result').html('');
					   }
					   // Activate group Finish Control
					   if(json.all_matches_finished){ scoring_board.activate_group_controls() }
				   }
				   else{ msg_type = 'danger'; }
				   if(json.msg != undefined){ scoring_board.show_alert(json.msg, msg_type); }
			   });
	},
	show_alert: function(content, type){
		if( scoring_board.alert_timer){ clearTimeout(scoring_board.alert_timer); }
		var msg_alert = '<div id="'+scoring_board.id_alert+'" class="alert';
		if(type){ msg_alert += ' alert-' + type; }
		msg_alert += ' fade in" ><a class="close" data-dismiss="alert" href="#">&times;</a>';
		msg_alert += content;
		msg_alert += '</div>';
		var alert = $('#'+scoring_board.id_alert_ctn);
		alert.html(msg_alert);
		alert.show();
		scoring_board.alert_timer = setTimeout("scoring_board.close_alert()", 5000);
    },
    close_alert: function(){
		$('#'+scoring_board.id_alert).alert('close');
    },
	activate_group_controls: function(){
		var group_control_item = $('#scoring-board-finish-group-controls');
		group_control_item.attr('href', scoring_board.url_finish_group);
		group_control_item.removeClass('disabled');
	},
};