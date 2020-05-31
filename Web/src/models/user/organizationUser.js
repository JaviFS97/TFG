// Models
import User from './user'
import PersonalUser from './personalUser'

// Firebase
import {db} from '@/firebase'

/**
 * Represents a organization user.
 */
export default class organizationUser extends User{

    /**
     * Basic constructor of organization user.
     * I added brackets in parameters for pass named parameters.
     * @param {String} email 
     * @param {String} password 
     * @param {String} nick 
     * @param {String} name 
     * @param {String} lastName 
     * @param {String} country 
     */
    constructor({email, password, name, parkingSpaces, coordenates}){
        super(email, password)
        this.name = name;
        this.parkingSpaces = parkingSpaces;
        this.coordenates = coordenates;
    }

    /**
     * Add a new organization user to Firebase database.
     * This methods add the information about user to 'organizations' and 'organizationsNames' collections. 
     * @param {Promise<UserCredential>} credentials of user.
     */
    async newOrganizationUserInDatabase(credentials){
        // Obtain user id from credentials 
        this.oid = credentials.user.uid

        // Add new user to the two collections, for this reason I use batch.
        let batch = db.batch()
        
        batch.set(db.collection('organizations').doc(this.oid), {
                                                         organizationName: this.name,
                                                         parkingSpaces:  this.parkingSpaces,
                                                         coordenateLAT: this.coordenates.lat,
                                                         coordenateLNG: this.coordenates.lng,
                                                        })
                                                        
        // let organizationNick = this.organizationName.toLowerCase()                                     
        batch.set(db.collection('organizationsNames').doc(this.name), {
                                                                oid: this.oid
                                                              })

        await batch.commit()

    }


    /**
     * Get uid of the loged user.
     */
    async getOID(){
        let organizationsNamesDoc = await db.collection('organizationsNames').doc(this.name).get()
        this.oid = organizationsNamesDoc.data().oid
    }


    async getOrganizationByOID(oid) {
        let organizationDoc = await db.collection('organizations').doc(oid).get()
        return organizationDoc.data()
    }

    /**
     * Obtain users that send a request to be part on this organization.
     */
    async getUsersRequest(){
        if (!this.oid)
            await this.getOID()     
               
        let usersRequest = []
        let requestOnDatabase = await db.collection('organizations').doc(this.oid).collection('userRequest').get()
        requestOnDatabase.forEach( request => {      
            let userRequest = {}
            userRequest.uid = request.id
            usersRequest.push(userRequest)
        })
        return usersRequest
    }

    /**
     * Obtain how many free spaces are there on this organization
     */
    async getNumberOfOccupiedParkingSpaces(){
        if (!this.oid)
            await this.getOID()    
        
        let occupiedParking = 0
        let membersOnDatabase = await db.collection('organizations').doc(this.oid).collection('members').get()
        membersOnDatabase.forEach( member => {      
            occupiedParking += Number(member.data().parkingSpaces)
        })        
        return occupiedParking
    }


    /**
     * If the admin of the organization accept the user with this uid.
     * @param {String} uid 
     * @param {Number} parkingSpaces 
     */
    async acceptUserRequest(uid, parkingSpaces){
        if (!this.oid)
            await this.getOID()    

        let batch = db.batch()
        batch.set(db.collection('organizations').doc(this.oid).collection('members').doc(uid), {
            parkingSpaces: parkingSpaces,
        })
        batch.delete(db.collection('organizations').doc(this.oid).collection('userRequest').doc(uid))
        batch.set(db.collection('users').doc(uid).collection('organizations').doc(this.oid), {
            requestStatus: 'ACCEPTED',
        })
        let numGaraje = 0
        while(numGaraje<parkingSpaces){
            batch.set(db.collection('users').doc(uid).collection('organizations').doc(this.oid).collection('parkings').doc(this.oid + numGaraje.toString()), {
                title: 'Parking ' + numGaraje.toString()
            })
            numGaraje++
        }

        await batch.commit()
    }


    async getMembers(){
        if (!this.oid)
            await this.getOID()    

        let members = []
        let membersOnDatabase = await db.collection('organizations').doc(this.oid).collection('members').get()
        membersOnDatabase.forEach( memberDB => {
            let member = {}
            member.uid = memberDB.id
            member.parkingSpaces = Number(memberDB.data().parkingSpaces)

            members.push(member)

        })        
        return members            
        
    }

    async getTimeLines(){
        if (!this.oid)
            await this.getOID()  
            
        let timeLines = []
        let membersOnDatabase = await db.collection('organizations').doc(this.oid).collection('timeLine').get()
        membersOnDatabase.forEach( time => {
            let timeLine = {}
            timeLine.date = time.data().date
            timeLine.plateURL = time.data().plateURL
            timeLine.status = time.data().status

            timeLines.push(timeLine)

        })        
        console.log(timeLines)
        return timeLines         
    }

}