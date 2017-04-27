import random

from flask_restful_swagger_2 import Api, swagger, Resource
from Trackster.libs.flask_get import *
from Trackster.utility.trackster_lib import *
from Trackster.Model.db_manager import *
from Trackster import configure as cfg
from Trackster.utility import API_return
from Trackster.Model.model_relationship import *


class CookiesREST(Resource):
    def get(self):
        return {
            "UserId": session_get("UserId"),
            "UserType": session_get("UserType")
        }

    def put(self):
        session["UserId"] = json_get("UserId")
        session["UserType"] = json_get("UserType")
        return "ok"


class HtmlRenderServiceTypeREST(Resource):
    def get(self):
        return {
            "SERVICE_TYPE": cfg.SERVICE_TYPE
        }


class OrderSinglePriceREST(Resource):
    @is_same_user
    @return_transform()
    @json_check_var(["Price"])
    def put(self, UserId, OrderId):
        Price = json_get("Price")
        return OrderManager().update_price(
            UserId, OrderId, Price
        )


class TempServiceREST(Resource):
    @is_same_user
    def get(self, UserId):
        UserType = session_get('UserType')
        sv = Service_Relationship(UserId, UserType)
        datas = sv.render_MyServices()
        return API_return.success({
            "Services": datas
        })


class TempServicesREST(Resource):
    @is_same_user
    def get(self, UserId):
        UserId = session_get('UserId')
        UserType = session_get('UserType')
        s = Service_Relationship(UserId, UserType)
        pg = ProGroup_Relationship(UserId, UserType)
        InGroupIds = pg.getInGroupProGroupIds()
        Services = s.render_Services(InGroupIds)
        return API_return.success({
            "Services": Services
        })


class TempServiceServiceIdREST(Resource):
    @is_same_user
    def get(self, UserId, ServiceId):
        Service = render_singleServiceInfo(UserId, ServiceId)
        return API_return.success({
            "Service": Service
        })


class TempPermissionREST(Resource):
    @is_same_user
    def get(self, UserId):
        UserId = session_get('UserId')
        UserType = session_get("UserType")

        pg = ProGroup_Relationship(UserId, UserType)
        permission = pg.getUserPermission()
        return API_return.success({
            "permission": permission
        })


class TempServiceServiceIdProGroupREST(Resource):
    @is_same_user
    def get(self, UserId, ServiceId):
        UserId = session_get('UserId')
        UserType = session_get("UserType")

        pg = ProGroup_Relationship(UserId, UserType)
        myProGroups = pg.displayMyGroupInfo_in_service(ServiceId)
        return API_return.success({
            "myProGroups": myProGroups
        })


class ServiceIdREST(Resource):
    def get(self, ServiceId):
        UserId = session_get('UserId')
        UserType = session_get("UserType")

        Service = render_singleServiceInfo(UserId, ServiceId)
        s = Service_Relationship(UserId, UserType)
        RelateServices = s.render_RelateServices(
            Service['ServiceId'],
            Service['UserId'],
            Service['Offering'],
            Service['ServiceType']
        )
        return API_return.success({
            "Services": Service,
            "RelateServices": RelateServices
        })

    @return_transform()
    @json_check_var(["update_data"])
    def put(self,ServiceId):
        UserId = session_get('UserId')
        UserType = session_get("UserType")
        update_data = json_get("update_data")

        service_manager = ServiceManager()
        return service_manager.update_service(UserId,ServiceId,update_data)


class ProjectIdTrackREST(Resource):
    def get(self, ProjectId):
        UserId = session_get('UserId')
        UserType = session_get("UserType")
        t = Tracks_Relationship(UserId, UserType)
        t_arr = t.display_ALL_tracks_by_Project(ProjectId)
        return API_return.success({
            "datas": t_arr
        })


class ServiceIdTrackREST(Resource):
    def get(self, ServiceId):
        UserId = session_get('UserId')
        UserType = session_get("UserType")
        tk = Tracks_Relationship(UserId, UserType)
        track_list = tk.getServiceId_to_Track(ServiceId)
        return API_return.success({
            "datas": track_list
        })


class TempNoticeREST(Resource):
    def get(self):
        UserId = session_get('UserId')
        UserType = session_get("UserType")

        n = Notice_Relationship(UserId, UserType)
        data = n.displayMyNotice()
        return API_return.success({
            "data": data
        })


class StatisticsREST(Resource):
    def get(self):
        UserId = session_get('UserId')
        UserType = session_get("UserType")

        # get connections count
        c = Comunity_Relationship(UserId, UserType)
        if UserType == 2:
            connection_artist_list = c.artist_display_connection_artistList()
            connection_studio_list = c.artist_display_connection_studioList()
        else:
            connection_artist_list = c.studio_display_connection_artistList()
            connection_studio_list = c.studio_display_connection_studioList()
        connection_count = len(connection_artist_list) + len(connection_studio_list)

        track_count = db.session.query(Tracks).filter(
            Tracks.UserId == UserId,
            Tracks.SoftDelete == 0,
        ).count()

        song_count = db.session.query(Tracks).filter(
            Tracks.UserId == UserId,
            Tracks.SoftDelete == 0,
            Tracks.InstrumentId == 6,
        ).count()

        p = Project_Relationship(UserId, UserType)
        Projects = p.render_project()

        service_count = db.session.query(Services).filter(
            Services.SoftDelete == 0,
            Services.UserId == UserId,
        ).count()

        return API_return.success({
            "tracks": track_count,
            "projects": len(Projects),
            "songs": song_count,
            "connections": connection_count,
            "service": service_count,
        })


class RecentProjectREST(Resource):
    def get(self):
        limitCount = args_get("limit", 4)
        UserId = session_get('UserId')
        UserType = session_get("UserType")
        pj = Project_Relationship(UserId, UserType)
        projectLists = pj.display_recent_project(limitCount)
        return API_return.success({
            "datas": projectLists
        })


class RecentServiceREST(Resource):
    def get(self):
        limitCount = args_get("limit", 4)
        UserId = session_get('UserId')
        UserType = session_get("UserType")
        sv = Service_Relationship(UserId, UserType)
        serviceLists = sv.display_recent_service(limitCount)
        return API_return.success({
            "datas": serviceLists
        })


class SuggestCollaboratorREST(Resource):
    def get(self):
        UserId = session_get('UserId')
        UserType = session_get("UserType")
        datas = []
        pg = ProGroup_Relationship(UserId, UserType)
        ProGroupIds = pg.getInGroupProGroupIds()
        if UserType == cfg.STUDIO_USERTYPE:
            datas = UserManager().get_company_info(UserId,ProGroupIds)
        if UserType == cfg.ARTIST_USERTYPE:
            datas = UserManager().get_user_info(UserId,ProGroupIds)
        return API_return.success({
            "datas": datas
        })


class MessageDashboardREST(Resource):
    def get(self):
        UserId = session_get('UserId')
        UserType = session_get("UserType")

        return API_return.success(
            MessageManager().get_dashboard_msg(UserId)
        )


class ServiceHotREST(Resource):
    def get(self):
        UserId = session_get('UserId')
        UserType = session_get("UserType")

        return API_return.success({
            "datas": ServiceManager().get_hot_service(UserId, UserType)
        })


class OrderIdTrackIdREST(Resource):
    @is_same_user
    def post(self, UserId, OrderId, TrackId):
        UserId = session_get('UserId')
        UserType = session_get("UserType")

        suc, msg, data = OrderTrackManager().add_ordertrack(OrderId, TrackId)
        if suc:
            service = OrderView.service(OrderId)
            order_manager = OrderManager()
            user_ids = order_manager.get_studios(OrderId)
            activity_manager = ActivityManager()
            for user_id in user_ids:
                activity_manager.add_order_track(
                    user_id,
                    OrderId,
                    service.ServiceTitle
                )
            return API_return.success()
        else:
            return API_return.other_error(msg)

    @is_same_user
    def delete(self, UserId, OrderId, TrackId):
        suc, msg, data = OrderTrackManager().delete_ordertrack(OrderId, TrackId)
        if suc:
            return API_return.success()
        else:
            return API_return.other_error(msg)


class OrderIdProcessTrack(Resource):
    @is_same_user
    def get(self, UserId, OrderId):
        UserId = session_get('UserId')
        UserType = session_get('UserType')
        t = Tracks_Relationship(UserId, UserType)
        track_list, process_track_list = t.display_tracks_by_Order(OrderId)
        return API_return.success({
            "track_list": track_list,
            "process_track_list": process_track_list
        })


class OrderIdCompleteREST(Resource):
    @is_same_user
    @json_check_var(["TrackIds"])
    def put(self, UserId, OrderId):
        """
        it do the things:
        - notice
        - update order
        - confirm leave track
        - leave track to buyer to copy to new track
        - new track to the project whtich is ordered
        :param UserId:
        :param OrderId:
        :return:
        """
        UserId = session_get('UserId')
        UserType = session_get('UserType')
        TrackIds = json_get("TrackIds")

        # notice and update order
        oTrk = Order_Realtionship(UserId, UserType)
        suc, msg = oTrk.Finish_the_Order(OrderId)
        if suc:
            ordertrack_manager = OrderTrackManager()
            suc, msg = ordertrack_manager.add_tracks(
                OrderId,
                TrackIds
            )
            if suc:
                return API_return.success()

        return API_return.other_error(msg)


class ActivityREST(Resource):
    def get(self):
        UserId = session_get('UserId')
        UserType = session_get('UserType')
        activity_manager = ActivityManager()
        return API_return.success({
            "datas": activity_manager.dashboard_view(UserId)
        })


class ActivityIdREST(Resource):
    @return_transform()
    def put(self, ActivityId):
        UserId = session_get('UserId')
        UserType = session_get('UserType')
        activity_manager = ActivityManager()
        return activity_manager.linked(ActivityId)


class TagREST(Resource):
    def get(self):
        UserId = session_get('UserId')
        return API_return.success({
            "datas": TagManager().get_user_all_tag(UserId)
        })

    @json_check_var(["Tags"])
    @return_transform("Tags")
    def post(self):
        tag_obj = json_get("Tags")
        UserId = session_get('UserId')
        tag_manager = TagManager()
        return tag_manager.add_tag(UserId, tag_obj)


class TagIdREST(Resource):
    @return_transform("Tags")
    def delete(self, TagId):
        UserId = session_get('UserId')
        tag_manager = TagManager()
        return tag_manager.delete_tag(UserId, TagId)


class CommunitySelfREST(Resource):
    def get(self):
        UserId = session_get('UserId')
        UserType = session_get('UserType')
        progroup_relation = ProGroup_Relationship(UserId, UserType)
        my_groups = progroup_relation.myProGroup()
        community = ComunityView.single(UserId, UserType)

        return {
            "Pro": True if my_groups else False,
            "Community": ComunityJSON(community)
        }

    @json_check_var(["update_data"])
    @return_transform("Community")
    def put(self):
        UserId = session_get('UserId')
        RoleId = session_get('UserType')
        update_data = json_get("update_data")
        comunity_manager = ComunityManager()
        return comunity_manager.update_single(UserId, RoleId, update_data)


class TagStudioREST(Resource):
    def get(self, StudioId):
        UserId = CompanyInfoes.query.filter(
            CompanyInfoes.CompanyId == StudioId
        ).scalar().UserId
        return API_return.success({
            "datas": TagManager().get_user_all_tag(UserId)
        })


class TagArtistIdREST(Resource):
    def get(self, ArtistId):
        UserId = UserInfoes.query.filter(
            UserInfoes.UserInfoId == ArtistId
        ).scalar().UserId
        return API_return.success({
            "datas": TagManager().get_user_all_tag(UserId)
        })


class CommunityArtistIdREST(Resource):
    def get(self,ArtistId):
        UserId = UserInfoes.query.filter(
            UserInfoes.UserInfoId == ArtistId
        ).scalar().UserId
        UserType = cfg.ARTIST_USERTYPE
        progroup_relation = ProGroup_Relationship(UserId, UserType)
        my_groups = progroup_relation.myProGroup()
        community = ComunityView.single(UserId, UserType)

        return {
            "Pro": True if my_groups else False,
            "Community": ComunityJSON(community)
        }


class CommunityStudioREST(Resource):
    def get(self,StudioId):
        UserId = CompanyInfoes.query.filter(
            CompanyInfoes.CompanyId == StudioId
        ).scalar().UserId
        UserType = cfg.STUDIO_USERTYPE
        progroup_relation = ProGroup_Relationship(UserId, UserType)
        my_groups = progroup_relation.myProGroup()
        community = ComunityView.single(UserId, UserType)

        return {
            "Pro": True if my_groups else False,
            "Community": ComunityJSON(community)
        }

class OrderIdInquiryREST(Resource):
    def get(self,OrderId):
        UserId = session_get('UserId')
        UserType = session_get('UserType')
        oInquery = OrderInquery_Relationship(UserId, UserType)
        Inquiry = oInquery.render_Inquery(OrderId)
        return API_return.success({
            "data":Inquiry
        })



class TestUserIdREST(Resource):
    def get(self,UserId):
        session_UserId = session_get("UserId")
        CHECK_USERID='6l2rPxF7slFY55r'
        if session_UserId==CHECK_USERID:
            multidata = UserInfoSbuquery.userInfo().filter(
                UserAccounts.UserId == UserId
            ).first()
            if multidata is None:
                return {
                    "msg":"no user"
                }
            result = UserMappingJSON(multidata)
            return result
        return {
            "msg":"wrong"
        }

