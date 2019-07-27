from django.shortcuts import render, redirect
from apps.log_reg_attack_app.models import User 
from apps.attack_app.models import HasAttacked

def Pirates(request):

    if 'user_id' not in request.session:
        return redirect('/')

    else: 
        this_pirate_attacker = User.objects.get(id=request.session['user_id'])
        print("**********this_pirate_attacker")
        print(this_pirate_attacker)
        this_pirate_alias = this_pirate_attacker.alias
        this_pirate_email = this_pirate_attacker.email
        other_pirates = User.objects.exclude(email=this_pirate_email)
        print("$$$$$$$$$this_pirate_attacker is logged in user-this is their query on their defend list:this_pirate_attacker.defend_list.all() returns a query set")
        num_wounds = this_pirate_attacker.defend_list.all()
        print(num_wounds)
        print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
        print("GOING TO LOOP THROUGH QUERYSET:")
        for  relationship in num_wounds:
            print("relationship.attacker:")
            print(relationship.attacker)
        print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")

        print("@@@@@@@@@@@print number which is len of the list of num_wounds...num_wounds is all of defend list")
        number = len(num_wounds)
        print(number)
        print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
        pirate_dict={}
        for pirate in other_pirates:
            #pirate.number_of_times _attacked = len(blah blah balh)
            pirate_dict [pirate.id] = len(pirate.defend_list.all())
        print("print the pirate dictionary")
        print(pirate_dict) 

        my_attack_list = this_pirate_attacker.attack_list.all()
        print("********** this_pirate_attacker attack_list")
        print(my_attack_list)

        # Landon's new code
        #logged_in_user is an object of User class returned by the query of User.objects.get(ide = request.session["user_id"])
        logged_in_user = User.objects.get(id = request.session["user_id"])
        #my_has_attacked_relationships is a local variable that is a queryset of instances of a HasAttacked object
        my_has_attacked_relationships = logged_in_user.defend_list.all()
        print("my_has_attacked_relationsihps$$$$$$$$$$$")
        print(my_has_attacked_relationships)
        print("END OF my_has_attacked_relationships$$$$$$$$$$$$$$$$$$")

        # Calculate total number of times I've been attacked
        sum_wounds = 0
        for relationship in my_has_attacked_relationships:
            sum_wounds += relationship.num_attacks

        context = {
            "sum_wounds": sum_wounds,
            "my_has_attacked_relationships" : my_has_attacked_relationships,


            "pirate_dictionary": pirate_dict,
            "this_pirate_attacker": this_pirate_attacker,
            "other_pirates": other_pirates,
            "this_pirate_alias": this_pirate_alias,
            "this_pirate_email": this_pirate_email,
            "my_attack_list": my_attack_list,
            "number": number,
                }
        return render(request,"attack_app/attack.html", context)


# CreateAttack takes in the pirate_id from the table on the attacks.html as a passed in paramter
#it then passes that pirate_id of the deferder pirate into the attack object


def CreateAttack(request, pirate_id):
    if 'user_id' not in request.session:
        return redirect('/')

    else:
        print("CreateAttack")
        print("******* pirate_id for defender******")
        print(pirate_id)
        this_pirate_defender = User.objects.get(id=pirate_id)        
        this_pirate_attacker = User.objects.get(id=request.session["user_id"])

        # If relationship already exists, just increment
        try:
            relationship_between_these_two = HasAttacked.objects.get(attacker_id = this_pirate_attacker.id, defender_id = this_pirate_defender.id)
            relationship_between_these_two.num_attacks += 1
            relationship_between_these_two.save()
        # If no relationship exists
        #then create a relationship...by creating a HasAttacked object 
        except:
            this_attack = HasAttacked.objects.create(attacker=this_pirate_attacker, defender=this_pirate_defender, num_attacks=1)

        return redirect ('/pirates_attack')

